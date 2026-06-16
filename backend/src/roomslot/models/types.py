from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import mapped_column

ID = Annotated[
    UUID,
    mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    ),
]

CreatedAt = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
]

UpdatedAt = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
]
