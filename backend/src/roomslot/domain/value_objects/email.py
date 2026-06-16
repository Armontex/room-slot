from attrs import define, field
from attrs_validation import validators as v
from email_validator import EmailNotValidError, validate_email

from roomslot.core.exceptions import DomainError


@define(frozen=True, slots=True)
class Email:
    value: str = field(
        converter=str.strip,
        validator=v.instance_of(str),
    )

    def __attrs_post_init__(self) -> None:
        try:
            normalized = validate_email(
                self.value,
                check_deliverability=False,
            ).normalized
        except EmailNotValidError as exc:
            raise DomainError("Invalid email") from exc

        object.__setattr__(self, "value", normalized.lower())
