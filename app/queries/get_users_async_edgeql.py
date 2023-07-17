# AUTOGENERATED FROM 'app/queries/get_users.edgeql' WITH:
#     $ edgedb-py
from __future__ import annotations

import dataclasses
import datetime
import uuid

import edgedb


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class GetUsersResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime


async def get_users(
        executor: edgedb.AsyncIOExecutor,
) -> list[GetUsersResult]:
    return await executor.query(
        """\
        select User {name, created_at};\
        """,
    )
