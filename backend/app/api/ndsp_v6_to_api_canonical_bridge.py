from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()

def canonical_path(path: str) -> str:
    if path.startswith("/api/v6/"):
        return path.replace("/api/v6/", "/api/", 1)
    return path

@router.api_route("/api/v6/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"], include_in_schema=False)
async def ndsp_v6_legacy_bridge(rest: str, request: Request):
    old_path = str(request.url.path)
    new_path = canonical_path(old_path)

    if old_path == new_path:
        return JSONResponse(status_code=410, content={
            "ok": False,
            "error": "DEPRECATED_V6_ROUTE",
            "message": "This /api/v6 route is deprecated. Use canonical /api route."
        })

    query = str(request.url.query or "")
    target = f"http://127.0.0.1:9001{new_path}"
    if query:
        target += "?" + query

    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as client:
            resp = await client.request(
                request.method,
                target,
                content=body,
                headers=headers,
            )

        content_type = resp.headers.get("content-type", "")
        if "application/json" in content_type:
            content = resp.json()
        else:
            content = {
                "ok": False,
                "raw": resp.text,
                "bridged_from": old_path,
                "bridged_to": new_path,
            }

        return JSONResponse(
            status_code=resp.status_code,
            content=content,
            headers={
                "X-NDSP-Deprecated-Route": old_path,
                "X-NDSP-Canonical-Route": new_path,
            }
        )
    except Exception as exc:
        return JSONResponse(status_code=502, content={
            "ok": False,
            "error": "V6_BRIDGE_FAILED",
            "detail": str(exc),
            "bridged_from": old_path,
            "bridged_to": new_path,
        })
