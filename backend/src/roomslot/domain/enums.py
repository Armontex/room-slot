from enum import StrEnum


class Building(StrEnum):
    MAB = "ГУК"
    RTF = "ИРИТ-РТФ"


class BookingStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
