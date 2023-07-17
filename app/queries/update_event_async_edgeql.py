# AUTOGENERATED FROM 'app/queries/update_event.edgeql' WITH:
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
class UpdateEventResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    address: str | None
    schedule: datetime.datetime | None
    host: UpdateEventResultHost | None


@dataclasses.dataclass
class UpdateEventResultHost(NoPydanticValidation):
    id: uuid.UUID
    name: str


async def update_event(
    executor: edgedb.AsyncIOExecutor,
    *,
    current_name: str,
    name: str,
    address: str,
    schedule: str,
    host_name: str,
) -> UpdateEventResult | None:
    return await executor.query_single(
        """\
        with current_name := <str>$current_name,
            new_name := <str>$name,
            address := <str>$address,
            schedule := <str>$schedule,
            host_name := <str>$host_name

        select (
            update Event filter .name = current_name
            set {
                name := new_name,
                address := address,
                schedule := <datetime>schedule,
                host := (select User filter .name = host_name)
            }
        ) {name, address, schedule, host: {name}};\
        """,
        current_name=current_name,
        name=name,
        address=address,
        schedule=schedule,
        host_name=host_name,
    )
