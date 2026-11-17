"""Workshop creation, participant booking and selected-identity reads in memory."""

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


def _workshop_field_errors(
    *, title: str, starts_at: datetime, ends_at: datetime, location: str, capacity: int
) -> dict[str, str]:
    """Shared field rules; retain the data model's existing exception messages."""
    errors = {}
    for name, value in (("title", title), ("location", location)):
        if not isinstance(value, str) or not value.strip():
            errors[name] = f"{name} must be non-empty text."
    if type(capacity) is not int or not 1 <= capacity <= 30:
        errors["capacity"] = "capacity must be an integer from 1 to 30."
    for name, value in (("starts_at", starts_at), ("ends_at", ends_at)):
        try:
            _require_aware(value, name)
        except ValueError as error:
            errors[name] = str(error)
    if (
        "starts_at" not in errors
        and "ends_at" not in errors
        and ends_at.astimezone(UTC) <= starts_at.astimezone(UTC)
    ):
        errors["ends_at"] = "ends_at must be later than starts_at."
    return errors


def _workshop_creation_policy_errors(
    *, starts_at: datetime | None, now: datetime, preparation_notes: str
) -> dict[str, str]:
    """Check creation-only rules; starts_at is already validated or absent."""
    errors = {}
    try:
        _require_aware(now, "now")
    except ValueError:
        errors["now"] = "The current server time is unavailable. Please try again."
    if (
        starts_at is not None
        and "now" not in errors
        and starts_at.astimezone(UTC) - now.astimezone(UTC) <= REGISTRATION_LEAD
    ):
        errors["starts_at"] = "Start must be more than 24 hours from submission."
    if not isinstance(preparation_notes, str):
        errors["preparation_notes"] = "Preparation notes must be text."
    return errors


def workshop_creation_errors(
    *,
    title: str,
    starts_at: datetime,
    ends_at: datetime,
    location: str,
    capacity: int,
    now: datetime,
    preparation_notes: str = "",
) -> dict[str, str]:
    """Return field feedback using the same rules as the creation operation."""
    messages = {
        "title must be non-empty text.": "Title is required.",
        "location must be non-empty text.": "Meeting point is required.",
        "capacity must be an integer from 1 to 30.": "Capacity must be a whole number from 1 to 30.",
        "starts_at must be a timezone-aware datetime.": "Choose a valid start date and time.",
        "ends_at must be a timezone-aware datetime.": "Choose a valid end date and time.",
        "ends_at must be later than starts_at.": "End date and time must be after the start.",
    }
    errors = {
        name: messages[message]
        for name, message in _workshop_field_errors(
            title=title, starts_at=starts_at, ends_at=ends_at, location=location, capacity=capacity
        ).items()
    }
    errors.update(
        _workshop_creation_policy_errors(
            starts_at=starts_at if "starts_at" not in errors else None,
            now=now,
            preparation_notes=preparation_notes,
        )
    )
    return errors


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
        for name in ("workshop_id", "owner_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text.")
        errors = _workshop_field_errors(
            title=self.title,
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            location=self.location,
            capacity=self.capacity,
        )
        if errors:
            raise ValueError(next(iter(errors.values())))

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
    try:
        workshop = Workshop(
            workshop_id=f"workshop-{state.next_workshop_id}",
            owner_id=actor.user_id,
            title=title.strip() if isinstance(title, str) else title,
            starts_at=starts_at,
            ends_at=ends_at,
            location=location.strip() if isinstance(location, str) else location,
            capacity=capacity,
            preparation_notes=(
                preparation_notes.strip()
                if isinstance(preparation_notes, str)
                else preparation_notes
            ),
        )
    except ValueError:
        return "INVALID_INPUT", state
    if _workshop_creation_policy_errors(
        starts_at=workshop.starts_at, now=now, preparation_notes=preparation_notes
    ):
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


def book_workshop(
    state: DemoState, actor: DemoUser | None, workshop_id: str, *, now: datetime
) -> tuple[str, DemoState]:
    """Book serially against the current state; never mutate the input snapshot."""
    permission = check_permission(state, actor, Role.PARTICIPANT)
    if permission != "OK":
        return permission, state
    workshop = next((w for w in state.workshops if w.workshop_id == workshop_id), None)
    if workshop is None:
        return "UNKNOWN_WORKSHOP", state
    try:
        _require_aware(now, "now")
    except ValueError:
        return "INVALID_INPUT", state
    now = now.astimezone(UTC)
    if now >= workshop.registration_cutoff.astimezone(UTC):
        return "REGISTRATION_CLOSED", state
    if any(
        row.workshop_id == workshop_id
        and row.participant_id == actor.user_id
        and row.status == RegistrationStatus.CONFIRMED
        for row in state.registrations
    ):
        return "DUPLICATE_ACTIVE", state
    if confirmed_count(state, workshop_id) >= workshop.capacity:
        return "FULL", state
    registration = Registration(
        registration_id=f"registration-{state.next_registration_id}",
        workshop_id=workshop_id,
        participant_id=actor.user_id,
        status=RegistrationStatus.CONFIRMED,
        created_at=now,
        updated_at=now,
    )
    return "OK", replace(
        state,
        users=state.users.copy(),
        workshops=state.workshops.copy(),
        registrations=[*state.registrations, registration],
        next_registration_id=state.next_registration_id + 1,
    )


def list_own_registrations(
    state: DemoState, actor: DemoUser | None
) -> tuple[str, tuple[Registration, ...]]:
    """Return this selected participant's records, including retained history."""
    permission = check_permission(state, actor, Role.PARTICIPANT)
    if permission != "OK":
        return permission, ()
    return "OK", tuple(row for row in state.registrations if row.participant_id == actor.user_id)


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
