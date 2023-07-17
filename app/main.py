from __future__ import annotations

import functools

import edgedb
from app import events
from app import users
from config.settings import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


async def setup_edgedb(app):
    client = app.state.edgedb = edgedb.create_async_client(
        host=settings.EDGEDB_HOST,
        port=settings.EDGEDB_PORT,
        user=settings.EDGEDB_USER,
        password=settings.EDGEDB_PASSWORD,
        database=settings.EDGEDB_DB,
        tls_ca=settings.EDGEDB_TLS_CA,
        tls_security="default",
    )
    await client.ensure_connected()


async def shutdown_edgedb(app):
    client, app.state.edgedb = app.state.edgedb, None
    await client.aclose()


def make_app():
    app = FastAPI()

    app.on_event("startup")(functools.partial(setup_edgedb, app))
    app.on_event("shutdown")(functools.partial(shutdown_edgedb, app))

    @app.get("/health_check", include_in_schema=False)
    async def health_check() -> dict[str, str]:
        return {"status": "Ok"}

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(events.router)
    app.include_router(users.router)

    return app


fast_api = make_app()
