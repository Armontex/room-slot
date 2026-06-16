from collections.abc import Callable
from typing import Any

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


def _all_column_names(constraint: Any, table: Table) -> str:
    return "_".join(column.name for column in constraint.columns.values())


_NAMING_CONVENTION: dict[str, Callable[[Any, Table], str] | str] = {
    "all_column_names": _all_column_names,
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "uq": "uq_%(table_name)s_%(all_column_names)s",
    "ix": "ix_%(table_name)s_%(all_column_names)s",
}


class Base(DeclarativeBase, MappedAsDataclass):
    metadata = MetaData(naming_convention=_NAMING_CONVENTION)
