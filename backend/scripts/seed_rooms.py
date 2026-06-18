from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from roomslot.common.providers import Uuid4Generator
from roomslot.config.settings import get_settings
from roomslot.db.models.room import RoomModel
from roomslot.domain.enums import Building

ROOMS: tuple[dict[str, Any], ...] = (
    {
        "name": "MAB-101",
        "building": Building.MAB,
        "floor": 1,
        "capacity": 4,
        "description": "Small study room for individual or pair work.",
    },
    {
        "name": "MAB-203",
        "building": Building.MAB,
        "floor": 2,
        "capacity": 8,
        "description": "Team room with a whiteboard.",
    },
    {
        "name": "MAB-305",
        "building": Building.MAB,
        "floor": 3,
        "capacity": 12,
        "description": "Large meeting room for group sessions.",
    },
    {
        "name": "RTF-214",
        "building": Building.RTF,
        "floor": 2,
        "capacity": 6,
        "description": "Quiet room for project discussions.",
    },
    {
        "name": "RTF-407",
        "building": Building.RTF,
        "floor": 4,
        "capacity": 10,
        "description": "Computer-equipped room for team work.",
    },
)


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.db.alembic_url)

    created = 0

    with Session(engine) as session:
        for room_data in ROOMS:
            exists_query = select(RoomModel.id).where(
                RoomModel.name == room_data["name"],
                RoomModel.building == room_data["building"],
                RoomModel.floor == room_data["floor"],
            )
            exists = session.execute(exists_query).scalar_one_or_none()

            if exists is not None:
                continue

            id = Uuid4Generator().generate()
            session.add(RoomModel(id=id, **room_data))
            created += 1

        session.commit()

    print(f"Seeded rooms: created={created}, total={len(ROOMS)}")


if __name__ == "__main__":
    main()
