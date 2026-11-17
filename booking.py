"""Framework-independent models and demo permission foundations.

Business operations are added in later accepted loops. Constructing a Workshop
represents data; it does not authorise creation or bypass the future lead-time rule.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from zoneinfo import ZoneInfo

WORKSHOP_TIMEZONE = ZoneInfo("Asia/Singapore")
REGISTRATION_LEAD = timedelta(hours=24)


class Role(StrEnum):
    PARTICIPANT = "PARTICIPANT"
    ORGANISER = "ORGANISER"


class RegistrationStatus(StrEnum):
    """V1.0 states only; waitlist states belong to the later CR-01 change."""

    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class DemoUser:
    user_id: str
    display_name: str
    role: Role


def _require_aware(value: datetime, field_name: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be a timezone-aware datetime.")


@dataclass(frozen=True)
class Workshop:
    workshop_id: str
    owner_id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str
    capacity: int
    preparation_notes: str = ""

    def __post_init__(self) -> None:
        for name in ("workshop_id", "owner_id", "title", "location"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text.")
        if type(self.capacity) is not int or not 1 <= self.capacity <= 30:
            raise ValueError("capacity must be an integer from 1 to 30.")
        _require_aware(self.starts_at, "starts_at")
        _require_aware(self.ends_at, "ends_at")
        if self.ends_at.astimezone(UTC) <= self.starts_at.astimezone(UTC):
            raise ValueError("ends_at must be later than starts_at.")

    @property
    def registration_cutoff(self) -> datetime:
        """Derive C using 24 elapsed hours and display the project's time zone."""
        return (self.starts_at.astimezone(UTC) - REGISTRATION_LEAD).astimezone(WORKSHOP_TIMEZONE)


@dataclass(frozen=True)
class Registration:
    registration_id: str
    workshop_id: str
    participant_id: str
    status: RegistrationStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        _require_aware(self.created_at, "created_at")
        _require_aware(self.updated_at, "updated_at")
        if self.updated_at.astimezone(UTC) < self.created_at.astimezone(UTC):
            raise ValueError("updated_at must not precede created_at.")


@dataclass
class DemoState:
    users: list[DemoUser] = field(default_factory=list)
    workshops: list[Workshop] = field(default_factory=list)
    registrations: list[Registration] = field(default_factory=list)
    next_workshop_id: int = 1
    next_registration_id: int = 1


def create_demo_state() -> DemoState:
    """Return independent mutable collections and fixed fictional identity data."""
    return DemoState(
        users=[
            DemoUser("participant-1", "Xingjian", Role.PARTICIPANT),
            DemoUser("participant-2", "Sam", Role.PARTICIPANT),
            DemoUser("organiser-1", "Rui Yan", Role.ORGANISER),
            DemoUser("organiser-2", "Alex", Role.ORGANISER),
        ]
    )


def resolve_actor(state: DemoState, user_id: str | None) -> DemoUser | None:
    """Resolve a selected ID to the session's fixed demo identity, or None."""
    return next((user for user in state.users if user.user_id == user_id), None)


def check_permission(
    state: DemoState,
    actor: DemoUser | None,
    required_role: Role,
    *,
    owner_id: str | None = None,
) -> str:
    """Return OK, INVALID_ACTOR or FORBIDDEN without changing state.

    Later operations must obtain owner_id from the looked-up target record.
    This helper does not look up targets or authenticate the selected person.
    """
    if actor is None:
        return "INVALID_ACTOR"
    canonical = resolve_actor(state, actor.user_id)
    if canonical is None or actor.role != canonical.role:
        return "INVALID_ACTOR"
    if canonical.role != required_role:
        return "FORBIDDEN"
    if owner_id is not None and canonical.user_id != owner_id:
        return "FORBIDDEN"
    return "OK"
