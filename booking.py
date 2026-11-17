"""Workshop creation, public browsing and owned rosters using session data."""

from dataclasses import dataclass, field, replace
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


def server_now() -> datetime:
    """Trusted application clock; tests may replace it without a user-facing control."""
    return datetime.now(UTC)


def create_workshop(
    state: DemoState,
    actor: DemoUser | None,
    *,
    title: str,
    starts_at: datetime,
    ends_at: datetime,
    location: str,
    capacity: int,
    now: datetime,
    preparation_notes: str = "",
) -> tuple[str, DemoState]:
    """Return an outcome and complete candidate state without mutating the input."""
    permission = check_permission(state, actor, Role.ORGANISER)
    if permission != "OK":
        return permission, state
    if not isinstance(preparation_notes, str):
        return "INVALID_INPUT", state
    try:
        _require_aware(now, "now")
        workshop = Workshop(
            workshop_id=f"workshop-{state.next_workshop_id}",
            owner_id=actor.user_id,
            title=title.strip() if isinstance(title, str) else title,
            starts_at=starts_at,
            ends_at=ends_at,
            location=location.strip() if isinstance(location, str) else location,
            capacity=capacity,
            preparation_notes=preparation_notes.strip(),
        )
    except ValueError:
        return "INVALID_INPUT", state
    if workshop.starts_at.astimezone(UTC) - now.astimezone(UTC) <= REGISTRATION_LEAD:
        return "INVALID_INPUT", state
    return "OK", replace(
        state,
        users=state.users.copy(),
        workshops=[*state.workshops, workshop],
        registrations=state.registrations.copy(),
        next_workshop_id=state.next_workshop_id + 1,
    )


def browse_workshops(state: DemoState) -> tuple[Workshop, ...]:
    """Public workshop information ordered by start instant, then stable ID."""
    return tuple(
        sorted(state.workshops, key=lambda w: (w.starts_at.astimezone(UTC), w.workshop_id))
    )


def confirmed_count(state: DemoState, workshop_id: str) -> int:
    return sum(
        row.workshop_id == workshop_id and row.status == RegistrationStatus.CONFIRMED
        for row in state.registrations
    )


def list_owned_workshops(
    state: DemoState, actor: DemoUser | None
) -> tuple[str, tuple[Workshop, ...]]:
    permission = check_permission(state, actor, Role.ORGANISER)
    if permission != "OK":
        return permission, ()
    return "OK", tuple(w for w in browse_workshops(state) if w.owner_id == actor.user_id)


def get_workshop_roster(
    state: DemoState, actor: DemoUser | None, workshop_id: str
) -> tuple[str, tuple[Registration, ...]]:
    """Check the actual target's stored owner before returning confirmed records."""
    workshop = next((w for w in state.workshops if w.workshop_id == workshop_id), None)
    permission = check_permission(
        state, actor, Role.ORGANISER, owner_id=workshop.owner_id if workshop is not None else None
    )
    if permission != "OK":
        return permission, ()
    if workshop is None:
        return "UNKNOWN_WORKSHOP", ()
    return "OK", tuple(
        row
        for row in state.registrations
        if row.workshop_id == workshop_id and row.status == RegistrationStatus.CONFIRMED
    )


def create_demo_data(now: datetime) -> DemoState:
    """Reconstruct valid fictional history once; all relative dates use this instant."""
    _require_aware(now, "now")
    now = now.astimezone(UTC)
    state = create_demo_state()
    anchor = now.astimezone(WORKSHOP_TIMEZONE).replace(minute=0, second=0, microsecond=0)
    created = now - timedelta(days=7)
    examples = [
        ("organiser-1", "Outdoor Navigation Basics", 72, 10, "North Trail Meeting Point"),
        ("organiser-2", "Outdoor Photography Walk", 96, 1, "Lakeside Entrance"),
        ("organiser-1", "Trail Safety Session", 12, 3, "Forest Visitor Centre"),
        ("organiser-2", "Past Nature Walk", -2, 2, "Riverside Shelter"),
    ]
    for owner_id, title, hours, capacity, location in examples:
        starts_at = anchor + timedelta(hours=hours)
        outcome, state = create_workshop(
            state,
            resolve_actor(state, owner_id),
            title=title,
            starts_at=starts_at,
            ends_at=starts_at + timedelta(hours=1),
            location=location,
            capacity=capacity,
            now=created,
            preparation_notes="Bring water, sun protection and closed-toe shoes. Follow organiser weather advice.",
        )
        if outcome != "OK":
            raise ValueError("Invalid demo workshop fixture.")
    for index, (workshop_id, participant_id, status) in enumerate(
        [
            ("workshop-1", "participant-1", RegistrationStatus.CONFIRMED),
            ("workshop-2", "participant-2", RegistrationStatus.CONFIRMED),
            ("workshop-3", "participant-1", RegistrationStatus.CONFIRMED),
            ("workshop-1", "participant-2", RegistrationStatus.CANCELLED),
        ],
        start=1,
    ):
        registered = created + timedelta(hours=index)
        state.registrations.append(
            Registration(
                f"registration-{index}",
                workshop_id,
                participant_id,
                status,
                registered,
                registered + timedelta(minutes=30)
                if status == RegistrationStatus.CANCELLED
                else registered,
            )
        )
    state.next_registration_id = len(state.registrations) + 1
    return state
