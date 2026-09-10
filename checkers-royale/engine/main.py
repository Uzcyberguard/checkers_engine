"""
ASGI entrypoint for the engine service.

Vercel Services builds this directory on its own and routes every /api/*
request here. The service receives the original path, so the routes below are
declared with their /api prefix rather than stripped.

All the real work lives in _lib; this file is only transport.
"""

import json
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from _lib.service import ROUTES, ApiError

app = FastAPI(
    title="Checkers Royale engine",
    description="Russian draughts move generation and alpha-beta search.",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

MAX_BODY = 64 * 1024


async def _payload(request: Request) -> Dict[str, Any]:
    if request.method == "GET":
        return dict(request.query_params)

    body = await request.body()
    if not body:
        return {}
    if len(body) > MAX_BODY:
        raise ApiError("request body too large", 413)
    try:
        parsed = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ApiError("request body must be valid JSON")
    if not isinstance(parsed, dict):
        raise ApiError("request body must be a JSON object")
    return parsed


@app.get("/api/health")
async def health() -> JSONResponse:
    return JSONResponse(
        {"ok": True, "endpoints": sorted(ROUTES)},
        headers={"Cache-Control": "no-store"},
    )


@app.api_route("/api/{action}", methods=["GET", "POST"])
async def run(action: str, request: Request) -> JSONResponse:
    handler = ROUTES.get(action)
    if handler is None:
        return JSONResponse(
            {"error": "no such endpoint: {}".format(action)}, status_code=404
        )

    try:
        payload = await _payload(request)
        result = handler(payload)
    except ApiError as exc:
        return JSONResponse({"error": exc.message}, status_code=exc.status)
    except Exception as exc:  # pragma: no cover - defensive
        return JSONResponse(
            {"error": "engine failure: {}".format(exc)}, status_code=500
        )

    return JSONResponse(result, headers={"Cache-Control": "no-store"})
