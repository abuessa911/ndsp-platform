#!/usr/bin/env python3
"""
NDSP Backend Contract V1.1 audit and regression harness.

Commands:
  audit          Inspect the V1.1 report, systemd unit, journal, source file, and ports.
  record         Extract curl cases from the report and create a contract baseline.
  verify         Replay the baseline and fail on contract regressions.
  install-timer  Install a hardened systemd timer for automatic verification.
  self-test      Run internal parser/schema checks without network access.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import gzip
import hashlib
import http.client
import json
import os
import pwd
import re
import shlex
import shutil
import socket
import ssl
import stat
import subprocess
import sys
import tempfile
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

VERSION = "1.1.1"
DEFAULT_SERVICE = "ndsp-live-decision-quality.service"
DEFAULT_SERVER = Path(
    "/home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py"
)
DEFAULT_REPORT_GLOB = (
    "/home/nawaf511/ndsp_reports/"
    "NDSP_DUAL_SCENARIO_DATA_QUALITY_BACKEND_V1_1_*/"
    "NDSP_DUAL_SCENARIO_DATA_QUALITY_BACKEND_V1_1_REPORT.md"
)
DEFAULT_BASELINE = Path.home() / ".local/state/ndsp-contract-v1-1/baseline.json"
DEFAULT_RESULT_DIR = Path.home() / "ndsp_reports/ndsp-contract-regression-v1-1"
SENSITIVE_HEADER_RE = re.compile(
    r"^(authorization|proxy-authorization|cookie|set-cookie|x-api-key|api-key)$",
    re.IGNORECASE,
)
SENSITIVE_QUERY_RE = re.compile(
    r"(token|secret|signature|api[_-]?key|authorization|password|session)",
    re.IGNORECASE,
)
VOLATILE_KEY_RE = re.compile(
    r"^(timestamp|time|date|datetime|generated_at|updated_at|created_at|"
    r"request_id|trace_id|correlation_id|span_id|latency|latency_ms|"
    r"duration|duration_ms|elapsed|nonce)$",
    re.IGNORECASE,
)
STABLE_VALUE_KEY_RE = re.compile(
    r"(contract|schema|api)?_?version$|^(type|kind|mode|source|status)$",
    re.IGNORECASE,
)
SCENARIO_TOKEN_RE = re.compile(
    r"(scenario|scenarios|baseline|alternative|candidate|proposed|"
    r"counterfactual|scenario_a|scenario_b|primary|secondary)",
    re.IGNORECASE,
)
QUALITY_TOKEN_RE = re.compile(
    r"(data[_-]?quality|quality|completeness|freshness|validity|accuracy|"
    r"coverage|missingness|consistency|timeliness|confidence)",
    re.IGNORECASE,
)
REPORT_SUSPICIOUS_RE = re.compile(
    r"\b(warn(?:ing)?|error|exception|traceback|failed?|skip(?:ped)?|"
    r"partial|unknown|degraded|timeout|fallback|rollback)\b",
    re.IGNORECASE,
)
SECRET_VALUE_RE = re.compile(
    r"(?i)(authorization:\s*(?:bearer|basic)\s+\S+|"
    r"(?:api[_-]?key|token|secret|password)\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{8,})"
)


class NdspError(RuntimeError):
    """Raised for actionable NDSP regression failures."""


@dataclasses.dataclass(slots=True)
class Finding:
    severity: str
    code: str
    message: str
    evidence: str = ""

    def as_dict(self) -> dict[str, str]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(slots=True)
class RequestCase:
    name: str
    method: str
    runtime_url: str
    manifest_url: str
    headers: dict[str, str]
    sensitive_headers: dict[str, str]
    body: str | None
    body_file: str | None
    timeout: float
    verify_tls: bool

    def headers_for_request(self) -> dict[str, str]:
        resolved = dict(self.headers)
        for header_name, env_name in self.sensitive_headers.items():
            value = os.environ.get(env_name)
            if value is None:
                raise NdspError(
                    f"Missing environment variable {env_name!r} "
                    f"for sensitive header {header_name!r}."
                )
            resolved[header_name] = value
        return resolved

    def body_bytes(self) -> bytes | None:
        if self.body_file:
            path = Path(os.path.expandvars(os.path.expanduser(self.body_file)))
            try:
                return path.read_bytes()
            except OSError as exc:
                raise NdspError(f"Cannot read request body file {path}: {exc}") from exc
        if self.body is None:
            return None
        return os.path.expandvars(self.body).encode("utf-8")

    def url_for_request(self) -> str:
        expanded = os.path.expandvars(self.manifest_url)
        if "$" in expanded:
            raise NdspError(
                f"Unresolved environment variable in URL for case {self.name}: "
                f"{self.manifest_url}"
            )
        return expanded

    def as_manifest_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "method": self.method,
            "url": self.manifest_url,
            "headers": self.headers,
            "sensitive_headers": self.sensitive_headers,
            "body": self.body,
            "body_file": self.body_file,
            "timeout": self.timeout,
            "verify_tls": self.verify_tls,
        }

    @classmethod
    def from_manifest_dict(cls, data: Mapping[str, Any]) -> "RequestCase":
        url = str(data["url"])
        return cls(
            name=str(data["name"]),
            method=str(data.get("method", "GET")).upper(),
            runtime_url=url,
            manifest_url=url,
            headers={str(k): str(v) for k, v in dict(data.get("headers", {})).items()},
            sensitive_headers={
                str(k): str(v)
                for k, v in dict(data.get("sensitive_headers", {})).items()
            },
            body=None if data.get("body") is None else str(data["body"]),
            body_file=(
                None if data.get("body_file") is None else str(data["body_file"])
            ),
            timeout=float(data.get("timeout", 15.0)),
            verify_tls=bool(data.get("verify_tls", True)),
        )


@dataclasses.dataclass(slots=True)
class HttpResult:
    status: int
    reason: str
    headers: dict[str, str]
    body: bytes
    elapsed_ms: float

    @property
    def content_type(self) -> str:
        return self.headers.get("content-type", "").split(";", 1)[0].strip().lower()

    def text(self) -> str:
        charset = "utf-8"
        content_type = self.headers.get("content-type", "")
        match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type, re.IGNORECASE)
        if match:
            charset = match.group(1)
        try:
            return self.body.decode(charset)
        except (LookupError, UnicodeDecodeError):
            return self.body.decode("utf-8", errors="replace")

    def json_value(self) -> Any:
        return json.loads(self.text())


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(
    command: Sequence[str],
    *,
    timeout: float = 20.0,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            list(command),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        if check:
            raise NdspError(f"Command failed: {shlex.join(command)}: {exc}") from exc
        return subprocess.CompletedProcess(command, 127, "", str(exc))
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        raise NdspError(
            f"Command failed ({result.returncode}): {shlex.join(command)}: {detail}"
        )
    return result


def find_latest_report(explicit: str | None) -> Path:
    if explicit:
        report = Path(explicit).expanduser().resolve()
        if not report.is_file():
            raise NdspError(f"Report does not exist: {report}")
        return report

    import glob

    matches = [Path(item) for item in glob.glob(DEFAULT_REPORT_GLOB)]
    matches = [item for item in matches if item.is_file()]
    if not matches:
        raise NdspError(
            "No V1.1 report found. Pass --report /absolute/path/to/report.md."
        )
    return max(matches, key=lambda item: item.stat().st_mtime_ns)


def parse_report_timestamp(path: Path) -> dt.datetime | None:
    match = re.search(r"_(\d{8})_(\d{6})(?:/|$)", str(path.parent))
    if not match:
        return None
    try:
        return dt.datetime.strptime(
            f"{match.group(1)}_{match.group(2)}", "%Y%m%d_%H%M%S"
        )
    except ValueError:
        return None


def normalize_shell_commands(text: str) -> list[str]:
    normalized = re.sub(r"\\\r?\n", " ", text)
    sources = re.findall(r"```(?:bash|sh|shell)?\s*(.*?)```", normalized, re.DOTALL)
    sources.append(normalized)

    commands: list[str] = []
    seen: set[str] = set()
    for source in sources:
        for raw_line in source.splitlines():
            if "curl" not in raw_line:
                continue
            match = re.search(r"(?:^|[\s$;])((?:sudo\s+)?curl\b.*)$", raw_line)
            if not match:
                continue
            command = match.group(1).strip()
            command = re.split(r"\s(?:\|\||&&|\||;)\s", command, maxsplit=1)[0]
            command = command.rstrip("` ")
            if command not in seen:
                seen.add(command)
                commands.append(command)
    return commands


def environment_name(prefix: str, key: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_").upper()
    return f"NDSP_{prefix}_{normalized}"


def sanitize_url(url: str) -> tuple[str, dict[str, str]]:
    parsed = urllib.parse.urlsplit(url)
    secrets: dict[str, str] = {}
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    sanitized_query: list[tuple[str, str]] = []
    for key, value in query:
        if SENSITIVE_QUERY_RE.search(key):
            env_name = environment_name("QUERY", key)
            secrets[env_name] = value
            sanitized_query.append((key, f"${{{env_name}}}"))
        else:
            sanitized_query.append((key, value))
    sanitized = urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urllib.parse.urlencode(sanitized_query, doseq=True, safe="${}"),
            parsed.fragment,
        )
    )
    return sanitized, secrets


def parse_curl_command(command: str, index: int) -> tuple[RequestCase, dict[str, str]]:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError as exc:
        raise NdspError(f"Cannot parse curl command: {command}: {exc}") from exc

    if tokens and tokens[0] == "sudo":
        tokens = tokens[1:]
    if not tokens or tokens[0] != "curl":
        raise NdspError(f"Not a curl command: {command}")

    method = ""
    url = ""
    headers: dict[str, str] = {}
    sensitive_headers_runtime: dict[str, str] = {}
    sensitive_header_env: dict[str, str] = {}
    body: str | None = None
    body_file: str | None = None
    timeout = 15.0
    verify_tls = True

    value_options = {
        "-X",
        "--request",
        "-H",
        "--header",
        "-d",
        "--data",
        "--data-raw",
        "--data-binary",
        "--data-urlencode",
        "--url",
        "--max-time",
        "--connect-timeout",
        "-u",
        "--user",
        "-o",
        "--output",
        "-w",
        "--write-out",
    }
    ignored_flags = {
        "-s",
        "--silent",
        "-S",
        "--show-error",
        "-f",
        "--fail",
        "--fail-with-body",
        "-L",
        "--location",
        "--compressed",
        "-i",
        "--include",
        "-I",
        "--head",
        "-k",
        "--insecure",
        "--http1.1",
        "--http2",
    }

    index_token = 1
    while index_token < len(tokens):
        token = tokens[index_token]
        option = token
        option_value: str | None = None

        if token.startswith("--") and "=" in token:
            option, option_value = token.split("=", 1)
        elif token in value_options:
            index_token += 1
            if index_token >= len(tokens):
                raise NdspError(f"Missing value for curl option {token}: {command}")
            option_value = tokens[index_token]

        if option in {"-X", "--request"}:
            method = str(option_value).upper()
        elif option in {"-H", "--header"}:
            header_text = str(option_value)
            if ":" not in header_text:
                raise NdspError(f"Invalid curl header {header_text!r}")
            name, value = header_text.split(":", 1)
            name = name.strip()
            value = value.strip()
            if SENSITIVE_HEADER_RE.match(name):
                env_name = environment_name("HEADER", name)
                sensitive_headers_runtime[name] = value
                sensitive_header_env[name] = env_name
            else:
                headers[name] = value
        elif option in {
            "-d",
            "--data",
            "--data-raw",
            "--data-binary",
            "--data-urlencode",
        }:
            data_value = str(option_value)
            if data_value.startswith("@"):
                body_file = data_value[1:]
            else:
                body = data_value
            if not method:
                method = "POST"
        elif option == "--url":
            url = str(option_value)
        elif option in {"--max-time", "--connect-timeout"}:
            try:
                timeout = max(timeout, float(str(option_value)))
            except ValueError as exc:
                raise NdspError(f"Invalid timeout {option_value!r}") from exc
        elif option in {"-u", "--user"}:
            env_name = "NDSP_CURL_BASIC_AUTH"
            sensitive_headers_runtime["Authorization"] = (
                "Basic "
                + __import__("base64").b64encode(
                    str(option_value).encode("utf-8")
                ).decode("ascii")
            )
            sensitive_header_env["Authorization"] = env_name
        elif option in {"-k", "--insecure"}:
            verify_tls = False
        elif option in {"-I", "--head"}:
            method = "HEAD"
        elif re.fullmatch(r"-[sSfLkiI]+", option):
            if "k" in option:
                verify_tls = False
            if "I" in option:
                method = "HEAD"
        elif option in {"-o", "--output", "-w", "--write-out"}:
            pass
        elif option.startswith("-"):
            if option not in ignored_flags and option not in value_options:
                raise NdspError(
                    f"Unsupported curl option {option!r}. "
                    "Add the case manually with --url if needed."
                )
        elif not url and re.match(r"^https?://", token):
            url = token

        index_token += 1

    if not url:
        for token in tokens:
            if re.match(r"^https?://", token):
                url = token
                break
    if not url:
        raise NdspError(f"No HTTP URL found in curl command: {command}")

    url = os.path.expandvars(url)
    if "$" in url:
        raise NdspError(f"Unresolved shell variable in curl URL: {url}")

    manifest_url, query_secrets = sanitize_url(url)
    parsed = urllib.parse.urlsplit(url)
    path_name = parsed.path.strip("/").replace("/", "_") or "root"
    host_name = parsed.hostname or "host"
    name = f"{index:02d}_{host_name}_{parsed.port or parsed.scheme}_{path_name}"
    method = method or ("POST" if body is not None or body_file else "GET")

    request_case = RequestCase(
        name=name,
        method=method,
        runtime_url=url,
        manifest_url=manifest_url,
        headers=headers,
        sensitive_headers=sensitive_header_env,
        body=body,
        body_file=body_file,
        timeout=timeout,
        verify_tls=verify_tls,
    )
    runtime_secrets = dict(query_secrets)
    for header_name, value in sensitive_headers_runtime.items():
        runtime_secrets[sensitive_header_env[header_name]] = value
    return request_case, runtime_secrets


def clean_extracted_url(raw_url: str) -> str:
    """Remove shell/Markdown delimiters accidentally captured after a URL."""
    return raw_url.rstrip(".,);]}>")


def extract_cases(report_text: str) -> tuple[list[RequestCase], dict[str, str], list[str]]:
    cases: list[RequestCase] = []
    secrets: dict[str, str] = {}
    warnings: list[str] = []
    seen: set[tuple[str, str, str | None]] = set()

    for index, command in enumerate(normalize_shell_commands(report_text), start=1):
        try:
            case, case_secrets = parse_curl_command(command, index)
        except NdspError as exc:
            warnings.append(str(exc))
            continue
        key = (case.method, case.runtime_url, case.body)
        if key in seen:
            continue
        seen.add(key)
        cases.append(case)
        secrets.update(case_secrets)

    if not cases:
        urls = re.findall(r"https?://[^\s<>`\"']+", report_text)
        for index, raw_url in enumerate(dict.fromkeys(urls), start=1):
            url = clean_extracted_url(raw_url)
            manifest_url, query_secrets = sanitize_url(url)
            parsed = urllib.parse.urlsplit(url)
            cases.append(
                RequestCase(
                    name=f"{index:02d}_{parsed.hostname or 'host'}_"
                    f"{parsed.port or parsed.scheme}_{parsed.path.strip('/') or 'root'}",
                    method="GET",
                    runtime_url=url,
                    manifest_url=manifest_url,
                    headers={},
                    sensitive_headers={},
                    body=None,
                    body_file=None,
                    timeout=15.0,
                    verify_tls=True,
                )
            )
            secrets.update(query_secrets)
        if cases:
            warnings.append(
                "No replayable curl commands were found; generated GET cases from URLs."
            )

    return cases, secrets, warnings


def decode_http_body(body: bytes, headers: Mapping[str, str]) -> bytes:
    encoding = headers.get("content-encoding", "").lower()
    if encoding == "gzip":
        return gzip.decompress(body)
    return body


def perform_request(case: RequestCase, *, use_runtime_values: bool = False) -> HttpResult:
    url = case.runtime_url if use_runtime_values else case.url_for_request()
    headers = case.headers_for_request()
    data = case.body_bytes()
    request = urllib.request.Request(
        url=url,
        data=data,
        headers=headers,
        method=case.method,
    )
    context: ssl.SSLContext | None = None
    if urllib.parse.urlsplit(url).scheme == "https":
        context = ssl.create_default_context()
        if not case.verify_tls:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

    started = dt.datetime.now(dt.timezone.utc)
    try:
        with urllib.request.urlopen(
            request,
            timeout=case.timeout,
            context=context,
        ) as response:
            status = int(response.status)
            reason = str(response.reason or "")
            response_headers = {
                key.lower(): value for key, value in response.headers.items()
            }
            body = decode_http_body(response.read(), response_headers)
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        reason = str(exc.reason or "")
        response_headers = {key.lower(): value for key, value in exc.headers.items()}
        body = decode_http_body(exc.read(), response_headers)
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        raise NdspError(
            f"{case.name}: request failed for {case.method} {url}: {exc}"
        ) from exc

    elapsed = dt.datetime.now(dt.timezone.utc) - started
    return HttpResult(
        status=status,
        reason=reason,
        headers=response_headers,
        body=body,
        elapsed_ms=elapsed.total_seconds() * 1000.0,
    )


def json_pointer_escape(segment: str) -> str:
    return segment.replace("~", "~0").replace("/", "~1")


def is_volatile_path(path: str) -> bool:
    segments = [segment for segment in path.split("/") if segment and segment != "*"]
    return any(VOLATILE_KEY_RE.match(segment.replace("~1", "/").replace("~0", "~")) for segment in segments)


def scalar_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def build_schema(
    value: Any,
    path: str = "",
    schema: dict[str, set[str]] | None = None,
    stable_values: dict[str, Any] | None = None,
) -> tuple[dict[str, set[str]], dict[str, Any]]:
    schema = schema if schema is not None else {}
    stable_values = stable_values if stable_values is not None else {}
    current_path = path or "/"
    if not is_volatile_path(current_path):
        schema.setdefault(current_path, set()).add(scalar_type(value))

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{json_pointer_escape(str(key))}"
            if is_volatile_path(child_path):
                continue
            build_schema(child, child_path, schema, stable_values)
            if (
                not isinstance(child, (dict, list))
                and "/*" not in child_path
                and STABLE_VALUE_KEY_RE.search(str(key))
                and len(str(child)) <= 200
            ):
                stable_values[child_path] = child
    elif isinstance(value, list):
        for child in value:
            child_path = f"{path}/*"
            build_schema(child, child_path, schema, stable_values)

    return schema, stable_values


def normalize_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: normalize_json(child)
            for key, child in sorted(value.items())
            if not VOLATILE_KEY_RE.match(str(key))
        }
    if isinstance(value, list):
        return [normalize_json(child) for child in value]
    return value


def walk_json(value: Any, path: str = "") -> Iterable[tuple[str, Any]]:
    yield path or "/", value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_json(child, f"{path}/{json_pointer_escape(str(key))}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_json(child, f"{path}/{index}")


def resolve_pointer(value: Any, pointer: str) -> tuple[bool, Any]:
    if pointer in {"", "/"}:
        return True, value
    current = value
    for raw_segment in pointer.lstrip("/").split("/"):
        segment = raw_segment.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and segment in current:
            current = current[segment]
        elif isinstance(current, list) and segment.isdigit():
            index = int(segment)
            if index >= len(current):
                return False, None
            current = current[index]
        else:
            return False, None
    return True, current


def semantic_evidence(
    value: Any,
    explicit_scenario_paths: Sequence[str] = (),
    explicit_quality_paths: Sequence[str] = (),
) -> dict[str, Any]:
    scenario_paths: set[str] = set()
    quality_paths: set[str] = set()
    key_names: set[str] = set()
    scenario_array_lengths: dict[str, int] = {}
    explicit_scenario_container_sizes: dict[str, int] = {}

    for path, child in walk_json(value):
        final_segment = path.rsplit("/", 1)[-1].replace("~1", "/").replace("~0", "~")
        key_names.add(final_segment.lower())
        if SCENARIO_TOKEN_RE.search(path):
            scenario_paths.add(path)
            if isinstance(child, list):
                scenario_array_lengths[path] = len(child)
        if QUALITY_TOKEN_RE.search(path):
            quality_paths.add(path)

    for pointer in explicit_scenario_paths:
        exists, child = resolve_pointer(value, pointer)
        if not exists:
            continue
        scenario_paths.add(pointer)
        if isinstance(child, list):
            scenario_array_lengths[pointer] = len(child)
            explicit_scenario_container_sizes[pointer] = len(child)
        elif isinstance(child, dict):
            explicit_scenario_container_sizes[pointer] = len(child)

    for pointer in explicit_quality_paths:
        exists, _ = resolve_pointer(value, pointer)
        if exists:
            quality_paths.add(pointer)

    dual_key_pairs = [
        {"baseline", "alternative"},
        {"baseline", "candidate"},
        {"baseline", "proposed"},
        {"baseline", "counterfactual"},
        {"scenario_a", "scenario_b"},
        {"scenario_1", "scenario_2"},
        {"primary", "secondary"},
        {"bullish", "bearish"},
        {"bull", "bear"},
        {"upside", "downside"},
        {"optimistic", "pessimistic"},
        {"best_case", "worst_case"},
        {"positive", "negative"},
    ]
    pair_evidence = [sorted(pair) for pair in dual_key_pairs if pair <= key_names]
    dual_by_array = any(length >= 2 for length in scenario_array_lengths.values())
    dual_by_explicit_container = any(
        size >= 2 for size in explicit_scenario_container_sizes.values()
    )
    dual_scenario = dual_by_array or dual_by_explicit_container or bool(pair_evidence)

    return {
        "scenario_paths": sorted(scenario_paths),
        "quality_paths": sorted(quality_paths),
        "scenario_array_lengths": scenario_array_lengths,
        "explicit_scenario_container_sizes": explicit_scenario_container_sizes,
        "dual_key_pairs": pair_evidence,
        "dual_scenario": dual_scenario,
    }


def create_snapshot(
    case: RequestCase,
    result: HttpResult,
    explicit_scenario_paths: Sequence[str],
    explicit_quality_paths: Sequence[str],
) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "status": result.status,
        "content_type": result.content_type,
        "elapsed_ms_at_record": round(result.elapsed_ms, 3),
        "body_size": len(result.body),
        "body_sha256": sha256_bytes(result.body),
        "json": False,
    }
    try:
        json_value = result.json_value()
    except (json.JSONDecodeError, UnicodeDecodeError):
        snapshot["text_sha256"] = sha256_bytes(result.text().strip().encode("utf-8"))
        return snapshot

    schema, stable_values = build_schema(json_value)
    normalized = json.dumps(
        normalize_json(json_value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    snapshot.update(
        {
            "json": True,
            "schema": {path: sorted(types) for path, types in sorted(schema.items())},
            "stable_values": stable_values,
            "normalized_json_sha256": sha256_bytes(normalized),
            "semantic": semantic_evidence(
                json_value,
                explicit_scenario_paths,
                explicit_quality_paths,
            ),
        }
    )
    return snapshot


def schema_for_current(value: Any) -> dict[str, set[str]]:
    schema, _ = build_schema(value)
    return schema


def compare_snapshot(
    case: RequestCase,
    baseline: Mapping[str, Any],
    current: HttpResult,
    max_latency_ms: float | None,
    explicit_scenario_paths: Sequence[str] = (),
    explicit_quality_paths: Sequence[str] = (),
) -> list[Finding]:
    findings: list[Finding] = []
    expected_status = int(baseline["status"])
    if current.status != expected_status:
        findings.append(
            Finding(
                "FAIL",
                "HTTP_STATUS_CHANGED",
                f"{case.name}: HTTP status changed from {expected_status} to {current.status}.",
            )
        )

    expected_content_type = str(baseline.get("content_type", ""))
    if expected_content_type and current.content_type != expected_content_type:
        findings.append(
            Finding(
                "FAIL",
                "CONTENT_TYPE_CHANGED",
                f"{case.name}: content type changed from "
                f"{expected_content_type!r} to {current.content_type!r}.",
            )
        )

    if max_latency_ms is not None and current.elapsed_ms > max_latency_ms:
        findings.append(
            Finding(
                "WARN",
                "LATENCY_THRESHOLD_EXCEEDED",
                f"{case.name}: {current.elapsed_ms:.1f} ms exceeds "
                f"{max_latency_ms:.1f} ms.",
            )
        )

    if not bool(baseline.get("json")):
        current_hash = sha256_bytes(current.text().strip().encode("utf-8"))
        if current_hash != baseline.get("text_sha256"):
            findings.append(
                Finding(
                    "FAIL",
                    "NON_JSON_BODY_CHANGED",
                    f"{case.name}: non-JSON response body changed.",
                )
            )
        return findings

    try:
        current_json = current.json_value()
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        findings.append(
            Finding(
                "FAIL",
                "JSON_BECAME_INVALID",
                f"{case.name}: response is no longer valid JSON: {exc}.",
            )
        )
        return findings

    current_schema = schema_for_current(current_json)
    for path, expected_types_raw in dict(baseline.get("schema", {})).items():
        expected_types = set(expected_types_raw)
        actual_types = current_schema.get(path)
        if actual_types is None:
            findings.append(
                Finding(
                    "FAIL",
                    "REQUIRED_PATH_REMOVED",
                    f"{case.name}: required schema path removed: {path}.",
                )
            )
        elif not expected_types.intersection(actual_types):
            findings.append(
                Finding(
                    "FAIL",
                    "TYPE_CHANGED",
                    f"{case.name}: {path} expected {sorted(expected_types)}, "
                    f"got {sorted(actual_types)}.",
                )
            )

    for pointer, expected_value in dict(baseline.get("stable_values", {})).items():
        exists, current_value = resolve_pointer(current_json, pointer)
        if not exists:
            continue
        if current_value != expected_value:
            findings.append(
                Finding(
                    "FAIL",
                    "STABLE_VALUE_CHANGED",
                    f"{case.name}: stable value at {pointer} changed from "
                    f"{expected_value!r} to {current_value!r}.",
                )
            )

    expected_semantic = dict(baseline.get("semantic", {}))
    current_semantic = semantic_evidence(
        current_json,
        explicit_scenario_paths,
        explicit_quality_paths,
    )
    if expected_semantic.get("dual_scenario") and not current_semantic["dual_scenario"]:
        findings.append(
            Finding(
                "FAIL",
                "DUAL_SCENARIO_CONTRACT_LOST",
                f"{case.name}: dual-scenario evidence disappeared.",
            )
        )
    if expected_semantic.get("quality_paths") and not current_semantic["quality_paths"]:
        findings.append(
            Finding(
                "FAIL",
                "DATA_QUALITY_CONTRACT_LOST",
                f"{case.name}: data-quality evidence disappeared.",
            )
        )

    return findings


def report_suspicious_lines(report_text: str) -> list[str]:
    suspicious: list[str] = []
    for line in report_text.splitlines():
        if not REPORT_SUSPICIOUS_RE.search(line):
            continue
        lower = line.lower()
        if re.fullmatch(r"\s*#{1,6}\s*rollback\s*", lower):
            continue
        if re.search(r"\b0\s+(?:warnings?|errors?|failures?|failed)\b", lower):
            continue
        if "[pass]" in lower and "rollback" not in lower:
            continue
        suspicious.append(line.strip())
    return suspicious[:50]


def tcp_check(host: str, port: int, timeout: float = 2.0) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, "connected"
    except OSError as exc:
        return False, str(exc)


def audit_report(report: Path, server: Path, service: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        report_text = report.read_text(encoding="utf-8")
    except OSError as exc:
        return [Finding("FAIL", "REPORT_UNREADABLE", f"Cannot read {report}: {exc}")]

    if not re.search(r"\bPASS\b", report_text):
        findings.append(
            Finding("FAIL", "REPORT_HAS_NO_PASS", "Report does not contain PASS.")
        )

    suspicious = report_suspicious_lines(report_text)
    for line in suspicious:
        findings.append(
            Finding("WARN", "REPORT_SUSPICIOUS_LINE", line[:500])
        )

    hashes = re.findall(r"\b[a-fA-F0-9]{64}\b", report_text)
    if not hashes:
        findings.append(
            Finding("WARN", "REPORT_HAS_NO_SHA256", "No SHA-256 value found in report.")
        )
    elif server.is_file():
        actual_hash = sha256_file(server)
        if actual_hash.lower() not in {item.lower() for item in hashes}:
            findings.append(
                Finding(
                    "FAIL",
                    "SERVER_HASH_MISMATCH",
                    f"Current server SHA-256 {actual_hash} is absent from the report.",
                )
            )

    required_markers = {
        "DIRECT_9057_NOT_EVIDENCED": r"\b9057\b",
        "WRAPPER_9082_NOT_EVIDENCED": r"\b9082\b",
        "PUBLIC_API_NOT_EVIDENCED": r"(public\s+api|api\s+public|البوابة|العامة)",
    }
    for code, pattern in required_markers.items():
        if not re.search(pattern, report_text, re.IGNORECASE):
            findings.append(
                Finding("WARN", code, f"Report lacks evidence matching {pattern!r}.")
            )

    if not re.search(r"\bHTTP/\d(?:\.\d)?\s+[1-5]\d\d\b|\bstatus(?:_code)?\b", report_text, re.IGNORECASE):
        findings.append(
            Finding(
                "WARN",
                "HTTP_STATUS_NOT_CAPTURED",
                "Report does not clearly capture HTTP status codes.",
            )
        )

    if not re.search(r"\b(400|401|403|404|409|422)\b|negative test|اختبار سلبي", report_text, re.IGNORECASE):
        findings.append(
            Finding(
                "WARN",
                "NO_NEGATIVE_CONTRACT_TEST",
                "No clear negative-path contract test is documented.",
            )
        )

    if SECRET_VALUE_RE.search(report_text):
        findings.append(
            Finding(
                "WARN",
                "POSSIBLE_SECRET_IN_REPORT",
                "Report may contain a credential or token; restrict its permissions.",
            )
        )

    cases, _, extraction_warnings = extract_cases(report_text)
    if not cases:
        findings.append(
            Finding(
                "FAIL",
                "NO_REPLAYABLE_HTTP_CASES",
                "No replayable curl commands or HTTP URLs found in report.",
            )
        )
    for warning in extraction_warnings:
        findings.append(Finding("WARN", "CASE_EXTRACTION_WARNING", warning))

    report_time = parse_report_timestamp(report)
    if report_time and server.is_file():
        server_time = dt.datetime.fromtimestamp(server.stat().st_mtime)
        if server_time > report_time + dt.timedelta(minutes=2):
            findings.append(
                Finding(
                    "FAIL",
                    "SERVER_NEWER_THAN_REPORT",
                    f"server.py mtime {server_time.isoformat()} is newer than "
                    f"report run {report_time.isoformat()}.",
                )
            )

    return findings


def audit_service(server: Path, service: str, report: Path) -> list[Finding]:
    findings: list[Finding] = []
    if shutil.which("systemctl") is None:
        return [Finding("WARN", "SYSTEMCTL_UNAVAILABLE", "systemctl is unavailable.")]

    properties = [
        "ActiveState",
        "SubState",
        "ExecMainStatus",
        "NRestarts",
        "User",
        "Group",
        "FragmentPath",
        "ExecStart",
        "StandardOutput",
        "StandardError",
        "NoNewPrivileges",
        "ProtectSystem",
        "ProtectHome",
    ]
    result = run_command(
        ["systemctl", "show", service, *[f"--property={item}" for item in properties]]
    )
    if result.returncode != 0:
        return [
            Finding(
                "FAIL",
                "SYSTEMD_SHOW_FAILED",
                result.stderr.strip() or result.stdout.strip(),
            )
        ]

    values: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value

    if values.get("ActiveState") != "active" or values.get("SubState") != "running":
        findings.append(
            Finding(
                "FAIL",
                "SERVICE_NOT_RUNNING",
                f"{service}: ActiveState={values.get('ActiveState')}, "
                f"SubState={values.get('SubState')}.",
            )
        )

    if values.get("ExecMainStatus") not in {"", "0"}:
        findings.append(
            Finding(
                "FAIL",
                "SERVICE_MAIN_STATUS_NONZERO",
                f"ExecMainStatus={values.get('ExecMainStatus')}.",
            )
        )

    try:
        restarts = int(values.get("NRestarts", "0") or "0")
    except ValueError:
        restarts = 0
    if restarts > 0:
        findings.append(
            Finding(
                "WARN",
                "SERVICE_RESTARTS_DETECTED",
                f"systemd reports NRestarts={restarts}.",
            )
        )

    service_user = values.get("User", "").strip()
    if not service_user:
        service_user = "root"

    if server.is_file():
        metadata = server.stat()
        owner = pwd.getpwuid(metadata.st_uid).pw_name
        owner_writable = bool(metadata.st_mode & stat.S_IWUSR)
        group_or_world_writable = bool(metadata.st_mode & (stat.S_IWGRP | stat.S_IWOTH))
        if service_user == "root" and owner != "root" and owner_writable:
            findings.append(
                Finding(
                    "FAIL",
                    "ROOT_SERVICE_RUNS_USER_WRITABLE_CODE",
                    f"{service} runs as root while {server} is writable by {owner}.",
                )
            )
        if group_or_world_writable:
            findings.append(
                Finding(
                    "FAIL",
                    "SERVER_CODE_TOO_WRITABLE",
                    f"{server} is group- or world-writable.",
                )
            )

    if values.get("NoNewPrivileges", "").lower() != "yes":
        findings.append(
            Finding(
                "WARN",
                "NO_NEW_PRIVILEGES_DISABLED",
                "systemd unit does not enable NoNewPrivileges=yes.",
            )
        )

    if values.get("ProtectSystem", "").lower() in {"", "no", "false"}:
        findings.append(
            Finding(
                "WARN",
                "PROTECT_SYSTEM_DISABLED",
                "systemd unit does not enable ProtectSystem.",
            )
        )

    since = parse_report_timestamp(report)
    if shutil.which("journalctl"):
        command = ["journalctl", "-u", service, "-p", "warning", "--no-pager", "-o", "short-iso"]
        if since:
            command.extend(["--since", since.strftime("%Y-%m-%d %H:%M:%S")])
        journal = run_command(command, timeout=20.0)
        journal_text = journal.stdout.strip()
        if journal.returncode == 0 and journal_text and "-- No entries --" not in journal_text:
            findings.append(
                Finding(
                    "WARN",
                    "POST_DEPLOY_WARNING_JOURNAL",
                    "Warning-or-higher journal entries exist after deployment.",
                    journal_text[-4000:],
                )
            )
        elif journal.returncode != 0:
            findings.append(
                Finding(
                    "WARN",
                    "JOURNAL_AUDIT_UNAVAILABLE",
                    journal.stderr.strip() or "Cannot inspect journal.",
                )
            )

    for port in (9057, 9082):
        ok, detail = tcp_check("127.0.0.1", port)
        if not ok:
            findings.append(
                Finding(
                    "FAIL",
                    f"PORT_{port}_UNREACHABLE",
                    f"127.0.0.1:{port} is unreachable: {detail}.",
                )
            )

    return findings


def finding_summary(findings: Sequence[Finding]) -> dict[str, int]:
    summary = {"FAIL": 0, "WARN": 0, "INFO": 0}
    for finding in findings:
        summary[finding.severity] = summary.get(finding.severity, 0) + 1
    return summary


def render_findings_markdown(
    title: str,
    findings: Sequence[Finding],
    metadata: Mapping[str, Any],
) -> str:
    summary = finding_summary(findings)
    lines = [
        f"# {title}",
        "",
        f"- Generated: `{iso_now()}`",
        f"- Failures: **{summary.get('FAIL', 0)}**",
        f"- Warnings: **{summary.get('WARN', 0)}**",
    ]
    for key, value in metadata.items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    if not findings:
        lines.append("## Result")
        lines.append("")
        lines.append("PASS — no findings.")
        return "\n".join(lines) + "\n"

    for severity in ("FAIL", "WARN", "INFO"):
        subset = [item for item in findings if item.severity == severity]
        if not subset:
            continue
        lines.extend(["", f"## {severity}"])
        for item in subset:
            lines.append(f"- **{item.code}** — {item.message}")
            if item.evidence:
                lines.append("")
                lines.append("  ```text")
                lines.extend(f"  {line}" for line in item.evidence.splitlines())
                lines.append("  ```")
    return "\n".join(lines) + "\n"


def atomic_write_text(path: Path, content: str, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        stream.write(content)
        temporary = Path(stream.name)
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def write_result_bundle(
    output_dir: Path,
    stem: str,
    findings: Sequence[Finding],
    metadata: Mapping[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    json_path = output_dir / f"{stem}_{timestamp}.json"
    markdown_path = output_dir / f"{stem}_{timestamp}.md"
    payload = {
        "generated_at": iso_now(),
        "summary": finding_summary(findings),
        "metadata": dict(metadata),
        "findings": [item.as_dict() for item in findings],
    }
    atomic_write_text(
        json_path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )
    atomic_write_text(
        markdown_path,
        render_findings_markdown(stem, findings, metadata),
    )

    for source, link_name in (
        (json_path, output_dir / f"{stem}_latest.json"),
        (markdown_path, output_dir / f"{stem}_latest.md"),
    ):
        try:
            link_name.unlink(missing_ok=True)
            link_name.symlink_to(source.name)
        except OSError:
            pass
    return markdown_path, json_path


def record_baseline(args: argparse.Namespace) -> int:
    report = find_latest_report(args.report)
    report_text = report.read_text(encoding="utf-8")
    if args.no_report_cases:
        cases: list[RequestCase] = []
        runtime_secrets: dict[str, str] = {}
        extraction_warnings: list[str] = []
    else:
        cases, runtime_secrets, extraction_warnings = extract_cases(report_text)

    seen_manual = {
        (case.method, case.runtime_url, case.body)
        for case in cases
    }
    for url in args.url:
        url = clean_extracted_url(url)
        manual_key = ("GET", url, None)
        if manual_key in seen_manual:
            continue
        seen_manual.add(manual_key)
        manifest_url, query_secrets = sanitize_url(url)
        parsed = urllib.parse.urlsplit(url)
        cases.append(
            RequestCase(
                name=f"manual_{len(cases) + 1:02d}_{parsed.hostname or 'host'}_"
                f"{parsed.port or parsed.scheme}_{parsed.path.strip('/') or 'root'}",
                method="GET",
                runtime_url=url,
                manifest_url=manifest_url,
                headers={},
                sensitive_headers={},
                body=None,
                body_file=None,
                timeout=args.timeout,
                verify_tls=not args.insecure,
            )
        )
        runtime_secrets.update(query_secrets)

    if not cases:
        raise NdspError(
            "No HTTP cases found. Add curl commands to the report or pass --url."
        )

    previous_env: dict[str, str | None] = {}
    for env_name, value in runtime_secrets.items():
        previous_env[env_name] = os.environ.get(env_name)
        os.environ[env_name] = value

    snapshots: list[dict[str, Any]] = []
    findings: list[Finding] = []
    try:
        for case in cases:
            if not case.verify_tls:
                findings.append(
                    Finding(
                        "WARN",
                        "TLS_VERIFICATION_DISABLED",
                        f"{case.name}: baseline preserves curl --insecure.",
                    )
                )
            try:
                result = perform_request(case, use_runtime_values=True)
            except NdspError as exc:
                findings.append(Finding("FAIL", "RECORD_REQUEST_FAILED", str(exc)))
                continue

            snapshot = create_snapshot(
                case,
                result,
                args.scenario_path,
                args.quality_path,
            )
            snapshots.append(
                {
                    "request": case.as_manifest_dict(),
                    "response": snapshot,
                }
            )
            if result.status < 200 or result.status >= 400:
                findings.append(
                    Finding(
                        "WARN",
                        "BASELINE_NON_SUCCESS_STATUS",
                        f"{case.name}: recorded HTTP {result.status}.",
                    )
                )
    finally:
        for env_name, old_value in previous_env.items():
            if old_value is None:
                os.environ.pop(env_name, None)
            else:
                os.environ[env_name] = old_value

    if not snapshots:
        raise NdspError("No baseline snapshots were created.")

    all_semantics = [
        item["response"].get("semantic", {})
        for item in snapshots
        if item["response"].get("json")
    ]
    has_dual = any(item.get("dual_scenario") for item in all_semantics)
    has_quality = any(item.get("quality_paths") for item in all_semantics)
    if not has_dual:
        findings.append(
            Finding(
                "FAIL",
                "DUAL_SCENARIO_NOT_DISCOVERED",
                "No dual-scenario evidence was discovered in recorded JSON. "
                "Use --scenario-path with the exact JSON Pointer if naming is custom.",
            )
        )
    if not has_quality:
        findings.append(
            Finding(
                "FAIL",
                "DATA_QUALITY_NOT_DISCOVERED",
                "No data-quality evidence was discovered in recorded JSON. "
                "Use --quality-path with the exact JSON Pointer if naming is custom.",
            )
        )

    manifest = {
        "format": "ndsp-contract-baseline-v1",
        "tool_version": VERSION,
        "created_at": iso_now(),
        "source_report": str(report),
        "source_report_sha256": sha256_file(report),
        "contract": "NDSP_DUAL_SCENARIO_DATA_QUALITY_BACKEND_V1_1",
        "explicit_scenario_paths": list(args.scenario_path),
        "explicit_quality_paths": list(args.quality_path),
        "cases": snapshots,
        "extraction_warnings": extraction_warnings,
        "required_environment_variables": sorted(runtime_secrets),
    }

    summary = finding_summary(findings)
    if summary["FAIL"] and not args.force:
        print(render_findings_markdown("NDSP baseline record", findings, {"report": report}))
        print(
            "Baseline was not written because contract evidence is incomplete. "
            "Use exact --scenario-path/--quality-path pointers, or --force only "
            "after manual review.",
            file=sys.stderr,
        )
        return 1

    baseline_path = Path(args.baseline).expanduser().resolve()
    atomic_write_text(
        baseline_path,
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

    print(f"Baseline: {baseline_path}")
    print(f"Cases: {len(snapshots)}")
    print(f"Dual scenario evidence: {'YES' if has_dual else 'NO'}")
    print(f"Data quality evidence: {'YES' if has_quality else 'NO'}")
    if runtime_secrets:
        print("Required environment variables:")
        for env_name in sorted(runtime_secrets):
            print(f"  {env_name}=<set securely; value was not stored>")
    for warning in extraction_warnings:
        print(f"WARN: {warning}")
    return 0 if summary["FAIL"] == 0 else 1


def verify_baseline(args: argparse.Namespace) -> int:
    baseline_path = Path(args.baseline).expanduser().resolve()
    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NdspError(f"Cannot load baseline {baseline_path}: {exc}") from exc

    if baseline.get("format") != "ndsp-contract-baseline-v1":
        raise NdspError(f"Unsupported baseline format in {baseline_path}.")

    findings: list[Finding] = []
    case_count = 0
    for item in baseline.get("cases", []):
        case_count += 1
        case = RequestCase.from_manifest_dict(item["request"])
        try:
            result = perform_request(case)
        except NdspError as exc:
            findings.append(Finding("FAIL", "REQUEST_FAILED", str(exc)))
            continue
        findings.extend(
            compare_snapshot(
                case,
                item["response"],
                result,
                args.max_latency_ms,
                baseline.get("explicit_scenario_paths", []),
                baseline.get("explicit_quality_paths", []),
            )
        )

    if case_count == 0:
        findings.append(
            Finding("FAIL", "BASELINE_HAS_NO_CASES", "Baseline contains no cases.")
        )

    metadata = {
        "baseline": str(baseline_path),
        "cases": case_count,
        "contract": baseline.get("contract", ""),
    }
    output_dir = Path(args.output_dir).expanduser().resolve()
    markdown_path, json_path = write_result_bundle(
        output_dir,
        "NDSP_CONTRACT_REGRESSION_V1_1",
        findings,
        metadata,
    )

    summary = finding_summary(findings)
    if summary["FAIL"]:
        print(
            f"FAIL: {summary['FAIL']} regression failure(s), "
            f"{summary['WARN']} warning(s)."
        )
    else:
        print(f"PASS: no contract regressions; {summary['WARN']} warning(s).")
    print(f"Report: {markdown_path}")
    print(f"JSON: {json_path}")
    return 1 if summary["FAIL"] else 0


def audit_command(args: argparse.Namespace) -> int:
    report = find_latest_report(args.report)
    server = Path(args.server).expanduser().resolve()
    findings = audit_report(report, server, args.service)
    findings.extend(audit_service(server, args.service, report))

    metadata = {
        "report": str(report),
        "server": str(server),
        "service": args.service,
    }
    output_dir = Path(args.output_dir).expanduser().resolve()
    markdown_path, json_path = write_result_bundle(
        output_dir,
        "NDSP_V1_1_AUDIT",
        findings,
        metadata,
    )
    summary = finding_summary(findings)
    print(render_findings_markdown("NDSP V1.1 audit", findings, metadata))
    print(f"Saved: {markdown_path}")
    print(f"JSON: {json_path}")
    return 1 if summary["FAIL"] else 0


def systemd_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def install_timer(args: argparse.Namespace) -> int:
    if os.geteuid() != 0:
        raise NdspError("install-timer must run through sudo.")

    script_path = Path(args.script_path).expanduser().resolve()
    baseline_path = Path(args.baseline).expanduser().resolve()
    if not script_path.is_file():
        raise NdspError(f"Script not found: {script_path}")
    if not baseline_path.is_file():
        raise NdspError(f"Baseline not found: {baseline_path}")

    run_as = args.run_as or os.environ.get("SUDO_USER")
    if not run_as or run_as == "root":
        raise NdspError("Pass --run-as USER; refusing to schedule regression as root.")
    try:
        account = pwd.getpwnam(run_as)
    except KeyError as exc:
        raise NdspError(f"Unknown user: {run_as}") from exc

    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = Path(account.pw_dir) / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    os.chown(output_dir, account.pw_uid, account.pw_gid)

    env_file = Path(account.pw_dir) / ".config/ndsp-contract-regression.env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    os.chown(env_file.parent, account.pw_uid, account.pw_gid)
    if not env_file.exists():
        env_file.write_text(
            "# Add required secrets as NAME=value. Keep mode 0600.\n",
            encoding="utf-8",
        )
        os.chmod(env_file, 0o600)
        os.chown(env_file, account.pw_uid, account.pw_gid)

    service_name = "ndsp-contract-regression-v1-1.service"
    timer_name = "ndsp-contract-regression-v1-1.timer"
    service_path = Path("/etc/systemd/system") / service_name
    timer_path = Path("/etc/systemd/system") / timer_name

    python_path = Path(sys.executable).resolve()
    exec_start = " ".join(
        [
            systemd_quote(str(python_path)),
            systemd_quote(str(script_path)),
            "verify",
            "--baseline",
            systemd_quote(str(baseline_path)),
            "--output-dir",
            systemd_quote(str(output_dir)),
            "--max-latency-ms",
            str(args.max_latency_ms),
        ]
    )
    service_content = textwrap.dedent(
        f"""\
        [Unit]
        Description=NDSP Backend Contract V1.1 Regression
        After=network-online.target {DEFAULT_SERVICE}
        Wants=network-online.target

        [Service]
        Type=oneshot
        User={run_as}
        Group={account.pw_gid}
        EnvironmentFile=-{env_file}
        ExecStart={exec_start}
        NoNewPrivileges=yes
        PrivateTmp=yes
        ProtectSystem=strict
        ProtectHome=read-only
        ReadWritePaths={output_dir}
        LockPersonality=yes
        RestrictSUIDSGID=yes
        UMask=0077
        """
    )
    timer_content = textwrap.dedent(
        f"""\
        [Unit]
        Description=Run NDSP Backend Contract V1.1 Regression Automatically

        [Timer]
        OnBootSec=5min
        OnUnitActiveSec={args.interval}
        RandomizedDelaySec=2min
        Persistent=true
        Unit={service_name}

        [Install]
        WantedBy=timers.target
        """
    )

    atomic_write_text(service_path, service_content, mode=0o644)
    atomic_write_text(timer_path, timer_content, mode=0o644)
    run_command(["systemctl", "daemon-reload"], check=True)
    run_command(["systemctl", "enable", "--now", timer_name], check=True)
    run_command(["systemctl", "start", service_name], check=False)

    print(f"Installed: {service_path}")
    print(f"Installed: {timer_path}")
    print(f"Environment: {env_file}")
    print(f"Results: {output_dir}")
    print(run_command(["systemctl", "list-timers", timer_name, "--no-pager"]).stdout)
    return 0


def self_test() -> int:
    sample_report = r"""
    # PASS
    curl -sS -X POST http://127.0.0.1:9057/v1/quality \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer secret-token' \
      --data '{"id":"test"}'
    curl -sS http://127.0.0.1:9082/health
    """
    cases, secrets, warnings = extract_cases(sample_report)
    assert len(cases) == 2, cases
    assert cases[0].method == "POST"
    assert "Authorization" in cases[0].sensitive_headers
    assert "NDSP_HEADER_AUTHORIZATION" in secrets
    assert not warnings

    sample_json = {
        "contract_version": "1.1",
        "scenarios": [{"name": "baseline"}, {"name": "alternative"}],
        "data_quality": {"completeness": 0.99},
        "timestamp": "volatile",
    }
    schema, stable = build_schema(sample_json)
    assert "/scenarios" in schema
    assert "/scenarios/*/name" in schema
    assert "/timestamp" not in schema
    assert stable["/contract_version"] == "1.1"
    semantic = semantic_evidence(sample_json)
    assert semantic["dual_scenario"]
    assert semantic["quality_paths"]

    custom_scenarios = {
        "comparison": {
            "expected": {"score": 1},
            "stressed": {"score": 0},
        },
        "dq": {"valid_rows": 10},
    }
    semantic = semantic_evidence(
        custom_scenarios,
        explicit_scenario_paths=["/comparison"],
        explicit_quality_paths=["/dq"],
    )
    assert semantic["dual_scenario"]
    assert semantic["quality_paths"]

    extracted, _, _ = extract_cases(
        "URL=http://127.0.0.1:9057/api/test?timeframe=weekly}"
    )
    assert extracted[0].runtime_url.endswith("weekly")
    assert not extracted[0].runtime_url.endswith("}")

    exists, value = resolve_pointer(sample_json, "/data_quality/completeness")
    assert exists and value == 0.99
    print("SELF-TEST PASS")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit and regression-test NDSP Backend Contract V1.1.",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Audit report and live service.")
    audit_parser.add_argument("--report")
    audit_parser.add_argument("--server", default=str(DEFAULT_SERVER))
    audit_parser.add_argument("--service", default=DEFAULT_SERVICE)
    audit_parser.add_argument("--output-dir", default=str(DEFAULT_RESULT_DIR))
    audit_parser.set_defaults(function=audit_command)

    record_parser = subparsers.add_parser(
        "record",
        help="Record a known-good baseline from curl cases in the report.",
    )
    record_parser.add_argument("--report")
    record_parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    record_parser.add_argument("--url", action="append", default=[])
    record_parser.add_argument(
        "--no-report-cases",
        action="store_true",
        help="Ignore HTTP cases extracted from the report and use only --url cases.",
    )
    record_parser.add_argument("--timeout", type=float, default=15.0)
    record_parser.add_argument("--insecure", action="store_true")
    record_parser.add_argument("--scenario-path", action="append", default=[])
    record_parser.add_argument("--quality-path", action="append", default=[])
    record_parser.add_argument(
        "--force",
        action="store_true",
        help="Write baseline despite missing semantic evidence.",
    )
    record_parser.set_defaults(function=record_baseline)

    verify_parser = subparsers.add_parser(
        "verify",
        help="Replay baseline and detect contract regressions.",
    )
    verify_parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    verify_parser.add_argument("--output-dir", default=str(DEFAULT_RESULT_DIR))
    verify_parser.add_argument("--max-latency-ms", type=float, default=3000.0)
    verify_parser.set_defaults(function=verify_baseline)

    install_parser = subparsers.add_parser(
        "install-timer",
        help="Install a hardened systemd timer for automatic checks.",
    )
    install_parser.add_argument("--script-path", required=True)
    install_parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    install_parser.add_argument("--run-as")
    install_parser.add_argument("--output-dir", default=str(DEFAULT_RESULT_DIR))
    install_parser.add_argument("--interval", default="15min")
    install_parser.add_argument("--max-latency-ms", type=float, default=3000.0)
    install_parser.set_defaults(function=install_timer)

    self_test_parser = subparsers.add_parser("self-test")
    self_test_parser.set_defaults(function=lambda _args: self_test())
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.function(args))
    except NdspError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("ERROR: interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
