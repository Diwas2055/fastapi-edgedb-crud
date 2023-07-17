import subprocess

import edgedb
import pytest
from app.main import make_app
from fastapi.testclient import TestClient
# from config import settings


def teardown_test_database():
    try:
        subprocess.run(
            ["bash", "./script/test_destroy_db.sh"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        pass


def setup_test_database():
    try:
        subprocess.run(["edgedb", "server", "stop"])
        subprocess.run(
            ["bash", "./script/test_create_db..sh"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        pass


@pytest.fixture
def test_client():
    with TestClient(make_app()) as client:
        yield client


@pytest.fixture
def tx_test_client(mocker):
    mocker.patch("app.main.setup_edgedb", tx_setup_edgedb)
    mocker.patch("app.main.shutdown_edgedb", tx_shutdown_edgedb)
    with TestClient(make_app()) as client:
        yield client


async def tx_setup_edgedb(app):
    setup_test_database()
    client = app.state.edgedb_client = edgedb.create_async_client()
    await client.ensure_connected()
    # client = make_app.state.edgedb = edgedb.create_async_client(
    #         host=settings.EDGEDB_HOST,
    #         port=settings.EDGEDB_PORT,
    #         user=settings.EDGEDB_USER,
    #         password=settings.EDGEDB_PASSWORD,
    #         database=settings.EDGEDB_DB_TEST,
    #         tls_ca=settings.EDGEDB_TLS_CA,
    #         tls_security="default",
    #     )
    # await make_app.ensure_connected()
    # subprocess.run(["edgedb"])
    # subprocess.run(["edgedb", "migrate", "-d", settings.EDGEDB_DB_TEST], check=True)

    async for tx in client.with_retry_options(edgedb.RetryOptions(0)).transaction():
        await tx.__aenter__()
        app.state.edgedb = tx
        break


async def tx_shutdown_edgedb(app):
    client, app.state.edgedb_client = app.state.edgedb_client, None
    tx, app.state.edgedb = app.state.edgedb, None
    await tx.__aexit__(Exception, Exception(), None)
    await client.aclose()
    teardown_test_database()
