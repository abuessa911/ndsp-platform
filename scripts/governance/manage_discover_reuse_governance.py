#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

POLICY = (
    ROOT
    / "governance"
    / "canonical-v1"
    / "NDSP_DISCOVER_REUSE_GOVERNANCE_V1_AR.md"
)

PRECEDENCE = (
    ROOT
    / "governance"
    / "canonical-v1"
    / "NDSP_GOVERNANCE_PRECEDENCE_V1.json"
)

ROOT_AGENTS = ROOT / "AGENTS.md"

POINTER_NAME = "NDSP_DISCOVER_REUSE_POLICY.md"

START = "<!-- NDSP_DISCOVER_REUSE_START -->"
END = "<!-- NDSP_DISCOVER_REUSE_END -->"

EXCLUDED_NAMES = {
    ".git",
    "node_modules",
    "vendor",
    "venv",
    ".venv",
    "__pycache__",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    ".next",
    ".vite",
    ".turbo",
    "dist",
    "build",
    "coverage",
    "runtime",
    "var",
    "tmp",
    "archive",
    "backups",
    "_backups",
    "artifacts",
}

ALLOWED_HIDDEN = {
    ".github",
    ".githooks",
}

MANAGED_BLOCK = f"""
{START}

## NDSP — البحث وإعادة الاستخدام قبل الإنشاء

قبل إنشاء أو إضافة أي:

- محرك
- خدمة
- API أو Gateway
- طبقة تحليلية
- صفحة أو مكوّن واجهة
- عقد أو Schema
- سياسة حوكمة
- اختبار
- أداة نشر أو تكامل

يجب تنفيذ التسلسل الإلزامي التالي:

1. **Discover** — البحث في المشروع والسجلات والعقود والخدمات.
2. **Reuse** — إعادة استخدام المكوّن القائم إن كان مناسبًا.
3. **Extend** — توسعة المكوّن القائم بدل إنشاء بديل.
4. **Merge** — دمج المكونات المتداخلة أو المتكررة.
5. **Create** — الإنشاء فقط بعد إثبات أن الخيارات السابقة غير كافية.
6. **Register** — تسجيل المالك والمسار والعقد والاختبارات والأدلة.

يحظر نسخ مكوّن قائم وتغيير اسمه فقط، أو إنشاء مالكين canonical
للوظيفة نفسها، أو إنشاء مكونات مشروع جديدة داخل `/opt`.

السياسة المركزية:

`governance/canonical-v1/NDSP_DISCOVER_REUSE_GOVERNANCE_V1_AR.md`

أي سياسة محلية يمكن أن تكون أشد، لكنها لا يجوز أن تلغي أو تخفف
هذه القاعدة.

{END}
""".strip()


POLICY_CONTENT = """# حوكمة NDSP للبحث وإعادة الاستخدام قبل الإنشاء

**معرف السياسة:** NDSP-GOV-DISCOVER-REUSE-001  
**الإصدار:** 1.0.0  
**الحالة:** إلزامية  
**النطاق:** المشروع كاملًا  
**تاريخ الاعتماد:** 2026-08-06

## 1. الهدف

منع إنشاء خدمات ومحركات وواجهات وعقود وسياسات متكررة، والمحافظة
على مالك ومسار canonical واحد لكل قدرة داخل المشروع.

## 2. التسلسل الإلزامي

قبل إنشاء أي مكوّن يجب تطبيق الترتيب التالي:

1. Discover — البحث والاكتشاف.
2. Reuse — إعادة الاستخدام.
3. Extend — توسعة الموجود.
4. Merge — دمج المتداخل أو المتكرر.
5. Create — الإنشاء كحل أخير.
6. Register — التسجيل والتوثيق.

لا يجوز الانتقال إلى خطوة لاحقة قبل توثيق عدم كفاية الخطوة السابقة.

## 3. نطاق البحث

يجب البحث في:

- أسماء الملفات والمجلدات.
- محتويات المصدر.
- AGENTS.md.
- ملفات الحوكمة canonical.
- العقود والمخططات.
- APIs والبوابات.
- ملفات systemd.
- اختبارات المشروع.
- سجلات القدرات والملكية.
- صفحات ومكونات الواجهة.
- المسارات القديمة والجديدة.
- تقارير الاكتشاف والتدقيق.

## 4. متطلبات الإنشاء الجديد

أي مكوّن جديد يجب أن يحدد:

- وصف الحاجة.
- الكلمات والمسارات التي تم البحث عنها.
- المكونات المرشحة الموجودة.
- سبب تعذر إعادة الاستخدام.
- سبب تعذر التوسعة أو الدمج.
- المالك canonical.
- المسار canonical.
- عقد الإدخال والإخراج.
- Validator.
- الاختبارات.
- سجل القدرة أو الخدمة.
- خطة Rollback إذا كان مكوّن Runtime.

## 5. المحظورات

يحظر:

- إنشاء خدمة مكررة.
- إنشاء محرك مكرر.
- إنشاء API مكرر.
- إنشاء طبقة مكررة.
- إنشاء صفحة تؤدي وظيفة قائمة.
- نسخ مكوّن وتغيير اسمه فقط.
- إنشاء عقد يناقض عقدًا قائمًا.
- إنشاء أكثر من مالك canonical للوظيفة نفسها.
- إنشاء مكونات مشروع جديدة داخل `/opt`.
- حذف خدمة دون أدلة المستهلكين وخطة انتقال.
- تخفيف هذه السياسة داخل مجلد فرعي.

## 6. الوراثة

تسري هذه السياسة على جميع مجلدات المشروع.

يمكن لملف AGENTS.md المحلي إضافة متطلبات أشد، لكنه لا يستطيع
إلغاء هذه السياسة أو تخفيفها.

## 7. الأولوية

هذه السياسة امتداد canonical للحوكمة الحالية، ولا تستبدل سياسات
الأمن أو البيانات الحقيقية أو العقود أو حوكمة الواجهة.

عند التعارض تطبق سياسة الأولوية المسجلة في:

`governance/canonical-v1/NDSP_GOVERNANCE_PRECEDENCE_V1.json`

## 8. الأدلة

لا يعتبر البحث مكتملًا بمجرد البحث باسم الملف فقط؛ يجب البحث أيضًا
بالوظيفة والمخرجات والعقود والمستهلكين والملكية.

عدم قراءة السياسة أو عدم ملاحظة وجودها لا يعفي من تطبيقها.
"""


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


def relative_link(target: Path, parent: Path) -> str:
    return os.path.relpath(target, parent)


def managed_directories() -> list[Path]:
    result: list[Path] = []

    for current, directories, _files in os.walk(
        ROOT,
        followlinks=False,
    ):
        current_path = Path(current)

        directories[:] = [
            name
            for name in directories
            if name not in EXCLUDED_NAMES
            and (
                not name.startswith(".")
                or name in ALLOWED_HIDDEN
            )
            and not (current_path / name).is_symlink()
        ]

        result.append(current_path)

    return sorted(set(result))


def update_managed_block(path: Path) -> str:
    if path.is_symlink():
        return "symlink-preserved"

    text = (
        path.read_text(encoding="utf-8", errors="ignore")
        if path.exists()
        else ""
    )

    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()

        updated = (
            f"{before}\n\n{MANAGED_BLOCK}\n\n{after}".rstrip()
            + "\n"
        )
        status = "updated"
    else:
        prefix = text.rstrip()

        updated = (
            f"{prefix}\n\n{MANAGED_BLOCK}\n"
            if prefix
            else f"{MANAGED_BLOCK}\n"
        )
        status = "added"

    path.write_text(updated, encoding="utf-8")
    return status


def backup_files() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    backup = (
        ROOT
        / "var"
        / "backups"
        / f"discover-reuse-governance-{timestamp}"
    )

    backup.mkdir(parents=True, exist_ok=True)

    for source in (ROOT_AGENTS, PRECEDENCE, POLICY):
        if source.exists() and not source.is_symlink():
            destination = backup / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    return backup


def write_policy() -> None:
    POLICY.parent.mkdir(parents=True, exist_ok=True)

    if POLICY.exists():
        existing = POLICY.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if "NDSP-GOV-DISCOVER-REUSE-001" not in existing:
            raise RuntimeError(
                f"يوجد ملف مختلف في المسار: {POLICY}"
            )

    POLICY.write_text(POLICY_CONTENT, encoding="utf-8")


def update_precedence() -> list[str]:
    if not PRECEDENCE.exists():
        raise RuntimeError(
            f"ملف الأولوية غير موجود: {PRECEDENCE}"
        )

    data = json.loads(
        PRECEDENCE.read_text(encoding="utf-8")
    )

    precedence = data.setdefault("precedence", [])
    rules = data.setdefault("rules", [])

    policy_relative = str(POLICY.relative_to(ROOT))

    if not any(
        item.get("path") == policy_relative
        for item in precedence
        if isinstance(item, dict)
    ):
        precedence.append(
            {
                "rank": 5,
                "path": policy_relative,
                "status": "OWNER_APPROVED_CANONICAL_EXTENSION",
            }
        )

    rule = "discover-reuse-extend-merge-create-register"

    if rule not in rules:
        rules.append(rule)

    PRECEDENCE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=4,
        )
        + "\n",
        encoding="utf-8",
    )

    missing: list[str] = []

    for item in precedence:
        if not isinstance(item, dict):
            continue

        path_value = item.get("path")

        if not path_value:
            continue

        target = ROOT / path_value

        if not target.exists():
            missing.append(path_value)

    return missing


def install_links() -> tuple[int, int, list[str]]:
    directories = managed_directories()

    linked = 0
    local_agents = 0
    conflicts: list[str] = []

    for directory in directories:
        agents = directory / "AGENTS.md"

        if directory == ROOT:
            update_managed_block(agents)

        elif lexists(agents):
            if agents.is_symlink():
                linked += 1
            elif agents.is_file():
                update_managed_block(agents)
                local_agents += 1
            else:
                conflicts.append(str(agents.relative_to(ROOT)))

        else:
            agents.symlink_to(
                relative_link(ROOT_AGENTS, directory)
            )
            linked += 1

        pointer = directory / POINTER_NAME
        expected = relative_link(POLICY, directory)

        if lexists(pointer):
            if pointer.is_symlink():
                if os.readlink(pointer) != expected:
                    pointer.unlink()
                    pointer.symlink_to(expected)
            elif pointer.is_file():
                conflicts.append(
                    str(pointer.relative_to(ROOT))
                )
        else:
            pointer.symlink_to(expected)

    return linked, local_agents, conflicts


def validate() -> list[str]:
    errors: list[str] = []

    if not POLICY.exists():
        errors.append(f"السياسة مفقودة: {POLICY}")

    if not ROOT_AGENTS.exists():
        errors.append("AGENTS.md الجذري مفقود.")
    else:
        text = ROOT_AGENTS.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if START not in text or END not in text:
            errors.append(
                "كتلة Discover-Reuse غير موجودة في AGENTS.md."
            )

    if not PRECEDENCE.exists():
        errors.append("ملف الأولوية مفقود.")
    else:
        data = json.loads(
            PRECEDENCE.read_text(encoding="utf-8")
        )

        policy_relative = str(POLICY.relative_to(ROOT))

        if not any(
            item.get("path") == policy_relative
            for item in data.get("precedence", [])
            if isinstance(item, dict)
        ):
            errors.append(
                "سياسة Discover-Reuse غير مسجلة في الأولوية."
            )

        if (
            "discover-reuse-extend-merge-create-register"
            not in data.get("rules", [])
        ):
            errors.append(
                "قاعدة Discover-Reuse غير مسجلة."
            )

    for directory in managed_directories():
        agents = directory / "AGENTS.md"
        pointer = directory / POINTER_NAME

        if not lexists(agents):
            errors.append(
                f"AGENTS.md مفقود: {directory.relative_to(ROOT)}"
            )

        if not pointer.is_symlink():
            errors.append(
                f"رابط السياسة مفقود: {directory.relative_to(ROOT)}"
            )
            continue

        try:
            if pointer.resolve() != POLICY.resolve():
                errors.append(
                    f"رابط سياسة غير صحيح: "
                    f"{pointer.relative_to(ROOT)}"
                )
        except OSError:
            errors.append(
                f"رابط تالف: {pointer.relative_to(ROOT)}"
            )

    return errors


def apply() -> int:
    if not ROOT_AGENTS.exists():
        raise RuntimeError("AGENTS.md الجذري غير موجود.")

    backup = backup_files()

    write_policy()
    update_managed_block(ROOT_AGENTS)

    missing_precedence_targets = update_precedence()

    linked, local_agents, conflicts = install_links()

    errors = validate()

    report = {
        "policy": str(POLICY.relative_to(ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "linked_agents": linked,
        "updated_local_agents": local_agents,
        "conflicts": conflicts,
        "missing_precedence_targets": missing_precedence_targets,
        "validation_errors": errors,
        "backup": str(backup.relative_to(ROOT)),
    }

    report_path = (
        ROOT
        / "governance"
        / "canonical-v1"
        / "NDSP_DISCOVER_REUSE_INSTALL_REPORT.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"policy={POLICY.relative_to(ROOT)}")
    print(f"backup={backup.relative_to(ROOT)}")
    print(f"linked_agents={linked}")
    print(f"updated_local_agents={local_agents}")
    print(f"conflicts={len(conflicts)}")

    if missing_precedence_targets:
        print("warning=missing_precedence_targets")

        for target in missing_precedence_targets:
            print(f"missing={target}")

    if errors:
        print("validation=FAIL")

        for error in errors:
            print(f"error={error}")

        return 1

    print("validation=PASS")
    return 0


def check() -> int:
    errors = validate()

    if errors:
        print("validation=FAIL")

        for error in errors:
            print(f"error={error}")

        return 1

    print("validation=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices={"apply", "check"},
    )

    args = parser.parse_args()

    if args.command == "apply":
        return apply()

    return check()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"fatal={error}", file=sys.stderr)
        raise SystemExit(1)
