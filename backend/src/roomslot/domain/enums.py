from enum import StrEnum


class Building(StrEnum):
    MAB = "ГУК"
    RTF = "ИРИТ-РТФ"


class BookingStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"
