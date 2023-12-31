# AUTOGENERATED FROM 'app/queries/create_event.edgeql' WITH:
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
class CreateEventResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    address: str | None
    schedule: datetime.datetime | None
    host: CreateEventResultHost | None


@dataclasses.dataclass
class CreateEventResultHost(NoPydanticValidation):
    id: uuid.UUID
    name: str


async def create_event(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
    address: str,
    schedule: str,
    host_name: str,
) -> CreateEventResult:
    return await executor.query_single(
        """\
        with name := <str>$name,
            address := <str>$address,
            schedule := <str>$schedule,
            host_name := <str>$host_name

        select (
            insert Event {
                name := name,
                address := address,
                schedule := <datetime>schedule,
                host := assert_single(
                    (select detached User filter .name = host_name)
                )
            }
        ) {name, address, schedule, host: {name}};\
        """,
        name=name,
        address=address,
        schedule=schedule,
        host_name=host_name,
    )
