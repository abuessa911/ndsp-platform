from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()

V1_CANONICAL_MAP = {
    "/api/v1/auth/register-trial": "/api/auth/register-trial",
    "/api/v1/trial/register": "/api/trial/register/ordinary",
    "/api/v1/trial/status": "/api/trial/status",
    "/api/v1/auth/login": "/api/auth/login",
}

def canonical_path(path: str) -> str:
    return V1_CANONICAL_MAP.get(path, path.replace("/api/v1/", "/api/", 1))

@router.api_route("/api/v1/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"], include_in_schema=False)
async def ndsp_v1_legacy_bridge(rest: str, request: Request):
    old_path = str(request.url.path)
    new_path = canonical_path(old_path)

    if new_path == old_path:
        return JSONResponse(status_code=410, content={
            "ok": False,
            "error": "DEPRECATED_V1_ROUTE",
            "message": "This /api/v1 route is deprecated. Use canonical /api route."
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
            resp = await client.request(request.method, target, content=body, headers=headers)

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
            },
        )
    except Exception as exc:
        return JSONResponse(status_code=502, content={
            "ok": False,
            "error": "V1_BRIDGE_FAILED",
            "detail": str(exc),
            "bridged_from": old_path,
            "bridged_to": new_path,
        })
