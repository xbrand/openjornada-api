"""Integration tests for the CORS allowlist (api/main.py).

Uses the default (no CORS_ALLOWED_ORIGINS set in the test environment)
development allowlist, which includes http://localhost:5173.
"""
from httpx import AsyncClient


async def test_allowed_origin_receives_cors_header(async_client: AsyncClient):
    response = await async_client.get("/", headers={"Origin": "http://localhost:5173"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


async def test_disallowed_origin_receives_no_cors_header(async_client: AsyncClient):
    response = await async_client.get("/", headers={"Origin": "http://evil.example.com"})
    assert "access-control-allow-origin" not in response.headers


def test_cors_config_never_combines_wildcard_with_credentials():
    from api.main import app, get_cors_allowed_origins

    assert "*" not in get_cors_allowed_origins()

    cors_middleware = next(
        m for m in app.user_middleware if m.cls.__name__ == "CORSMiddleware"
    )
    # starlette 1.x replaced Middleware.options with args/kwargs
    options = getattr(cors_middleware, "options", None)
    if options is None:
        options = cors_middleware.kwargs
    assert "*" not in options["allow_origins"]
    assert options["allow_credentials"] is True
