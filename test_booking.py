"""L1 foundation checks; these do not complete the planned B/W/I scenarios."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from streamlit.testing.v1 import AppTest

from booking import (
    WORKSHOP_TIMEZONE,
    Registration,
    RegistrationStatus,
    Role,
    Workshop,
    create_demo_state,
)

APP_PATH = Path(__file__).with_name("app.py")


@pytest.fixture
def workshop() -> Workshop:
    return Workshop(
        workshop_id="workshop-1",
        owner_id="organiser-1",
        title="Outdoor Navigation",
        starts_at=datetime(2026, 12, 10, 9, tzinfo=WORKSHOP_TIMEZONE),
        ends_at=datetime(2026, 12, 10, 12, tzinfo=WORKSHOP_TIMEZONE),
        location="North Trail Meeting Point",
        capacity=10,
    )


def test_state_factories_do_not_share_lists_or_counters(workshop: Workshop) -> None:
    first = create_demo_state()
    second = create_demo_state()
    created = datetime(2026, 12, 1, tzinfo=UTC)
    first.users.pop()
    first.workshops.append(workshop)
    first.registrations.append(
        Registration(
            "registration-1",
            "workshop-1",
            "participant-1",
            RegistrationStatus.CONFIRMED,
            created,
            created,
        )
    )
    first.next_workshop_id = 2
    first.next_registration_id = 2

    assert len(second.users) == 4
    assert second.workshops == []
    assert second.registrations == []
    assert second.next_workshop_id == 1
    assert second.next_registration_id == 1
    assert first.users is not second.users
    assert first.workshops is not second.workshops
    assert first.registrations is not second.registrations


def test_fictional_identity_data_uses_unique_stable_ids_and_both_roles() -> None:
    users = create_demo_state().users
    assert [user.user_id for user in users] == [
        "participant-1",
        "participant-2",
        "organiser-1",
        "organiser-2",
    ]
    assert {user.role for user in users} == {Role.PARTICIPANT, Role.ORGANISER}
    assert len({user.user_id for user in users}) == len(users)


@pytest.mark.parametrize("capacity", [1, 30])
def test_workshop_represents_valid_capacity_boundaries(workshop: Workshop, capacity: int) -> None:
    assert replace(workshop, capacity=capacity).capacity == capacity


@pytest.mark.parametrize("capacity", [0, -1, 31, 1.5, True, False, "10", None])
def test_workshop_rejects_invalid_capacity(workshop: Workshop, capacity: object) -> None:
    with pytest.raises(ValueError, match="capacity must be an integer from 1 to 30"):
        replace(workshop, capacity=capacity)
    assert workshop.capacity == 10


@pytest.mark.parametrize("field_name", ["workshop_id", "owner_id", "title", "location"])
@pytest.mark.parametrize("value", [" ", None])
def test_workshop_rejects_missing_required_text(
    workshop: Workshop, field_name: str, value: object
) -> None:
    with pytest.raises(ValueError, match=f"{field_name} must be non-empty text"):
        replace(workshop, **{field_name: value})


@pytest.mark.parametrize("field_name", ["starts_at", "ends_at"])
@pytest.mark.parametrize("value", [datetime(2026, 12, 10, 9), None])
def test_workshop_rejects_naive_or_missing_instants(
    workshop: Workshop, field_name: str, value: object
) -> None:
    with pytest.raises(ValueError, match=f"{field_name} must be a timezone-aware datetime"):
        replace(workshop, **{field_name: value})


@pytest.mark.parametrize("offset", [timedelta(), timedelta(seconds=-1)])
def test_workshop_rejects_non_positive_duration(workshop: Workshop, offset: timedelta) -> None:
    with pytest.raises(ValueError, match="ends_at must be later"):
        replace(workshop, ends_at=workshop.starts_at + offset)


def test_cutoff_is_twenty_four_elapsed_hours_before_start(workshop: Workshop) -> None:
    assert workshop.registration_cutoff == datetime(2026, 12, 9, 9, tzinfo=WORKSHOP_TIMEZONE)
    assert workshop.registration_cutoff.tzinfo == WORKSHOP_TIMEZONE
    assert workshop.starts_at.astimezone(UTC) - workshop.registration_cutoff.astimezone(UTC) == (
        timedelta(hours=24)
    )


def test_data_model_can_represent_historical_workshops(workshop: Workshop) -> None:
    historical = replace(
        workshop,
        starts_at=datetime(2020, 1, 1, 9, tzinfo=WORKSHOP_TIMEZONE),
        ends_at=datetime(2020, 1, 1, 12, tzinfo=WORKSHOP_TIMEZONE),
    )
    assert historical.registration_cutoff == datetime(2019, 12, 31, 9, tzinfo=WORKSHOP_TIMEZONE)


@pytest.mark.parametrize("reverse", [False, True], ids=["chronological", "reversed"])
def test_workshop_orders_repeated_clock_times_by_instant(workshop: Workshop, reverse: bool) -> None:
    zone = ZoneInfo("America/New_York")
    first = datetime(2026, 11, 1, 1, 30, tzinfo=zone, fold=0)
    second = datetime(2026, 11, 1, 1, 15, tzinfo=zone, fold=1)
    assert second.astimezone(UTC) - first.astimezone(UTC) == timedelta(minutes=45)
    if reverse:
        with pytest.raises(ValueError, match="ends_at must be later"):
            replace(workshop, starts_at=second, ends_at=first)
    else:
        result = replace(workshop, starts_at=first, ends_at=second)
        assert result.ends_at.astimezone(UTC) > result.starts_at.astimezone(UTC)


@pytest.mark.parametrize("reverse", [False, True], ids=["chronological", "reversed"])
def test_registration_orders_repeated_clock_times_by_instant(reverse: bool) -> None:
    zone = ZoneInfo("America/New_York")
    first = datetime(2026, 11, 1, 1, 30, tzinfo=zone, fold=0)
    second = datetime(2026, 11, 1, 1, 15, tzinfo=zone, fold=1)
    assert second.astimezone(UTC) - first.astimezone(UTC) == timedelta(minutes=45)
    if reverse:
        with pytest.raises(ValueError, match="updated_at must not precede"):
            Registration("r-1", "w-1", "participant-1", RegistrationStatus.CONFIRMED, second, first)
    else:
        result = Registration(
            "r-1", "w-1", "participant-1", RegistrationStatus.CONFIRMED, first, second
        )
        assert result.updated_at.astimezone(UTC) > result.created_at.astimezone(UTC)


@pytest.mark.parametrize("field_name", ["created_at", "updated_at"])
def test_registration_rejects_naive_timestamps(field_name: str) -> None:
    created = datetime(2026, 12, 1, tzinfo=UTC)
    original = Registration(
        "r-1", "w-1", "participant-1", RegistrationStatus.CONFIRMED, created, created
    )
    with pytest.raises(ValueError, match=f"{field_name} must be a timezone-aware datetime"):
        replace(original, **{field_name: created.replace(tzinfo=None)})


def test_registration_rejects_update_before_creation() -> None:
    created = datetime(2026, 12, 1, tzinfo=UTC)
    with pytest.raises(ValueError, match="updated_at must not precede"):
        Registration(
            "r-1",
            "w-1",
            "participant-1",
            RegistrationStatus.CONFIRMED,
            created,
            created - timedelta(seconds=1),
        )


@pytest.mark.parametrize("view", ["Workshops", "My Bookings", "Organiser"])
def test_app_views_start_without_exception(view: str) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.sidebar.radio(key="current_view").set_value(view).run()
    assert not app.exception
    assert app.subheader[0].value == view
    assert app.metric[0].value == "0"
    assert app.metric[1].value == "0"


def test_app_refresh_and_navigation_preserve_session_state(workshop: Workshop) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    state = app.session_state.demo_state
    state.workshops.append(workshop)
    state.next_workshop_id = 2
    app.sidebar.button(key="refresh_view").click().run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()

    assert not app.exception
    assert app.session_state.demo_state is state
    assert app.session_state.demo_state.workshops == [workshop]
    assert app.session_state.demo_state.next_workshop_id == 2
    assert app.metric[0].value == "1"


def test_independent_app_sessions_do_not_share_state(workshop: Workshop) -> None:
    first = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    second = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    first.session_state.demo_state.workshops.append(workshop)
    first.session_state.demo_state.next_workshop_id = 2
    first.run()
    second.run()

    assert not first.exception
    assert not second.exception
    assert first.metric[0].value == "1"
    assert second.metric[0].value == "0"
    assert second.session_state.demo_state.workshops == []
    assert second.session_state.demo_state.next_workshop_id == 1
