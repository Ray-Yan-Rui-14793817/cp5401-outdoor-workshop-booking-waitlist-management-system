"""Retained L1 regressions and L2 identity/permission foundation checks."""

from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from streamlit.testing.v1 import AppTest

from booking import (
    WORKSHOP_TIMEZONE,
    DemoState,
    DemoUser,
    Registration,
    RegistrationStatus,
    Role,
    Workshop,
    check_permission,
    create_demo_state,
    resolve_actor,
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


@pytest.mark.parametrize(
    ("starts_at", "expected_cutoff"),
    [
        (
            datetime(2026, 12, 10, 9, tzinfo=WORKSHOP_TIMEZONE),
            datetime(2026, 12, 9, 9, tzinfo=WORKSHOP_TIMEZONE),
        ),
        (
            datetime(2026, 11, 1, 9, tzinfo=ZoneInfo("America/New_York")),
            datetime(2026, 10, 31, 22, tzinfo=WORKSHOP_TIMEZONE),
        ),
        (
            datetime(2026, 3, 8, 9, tzinfo=ZoneInfo("America/New_York")),
            datetime(2026, 3, 7, 21, tzinfo=WORKSHOP_TIMEZONE),
        ),
    ],
    ids=["singapore", "fall-back", "spring-forward"],
)
def test_cutoff_is_twenty_four_elapsed_hours_before_start(
    workshop: Workshop, starts_at: datetime, expected_cutoff: datetime
) -> None:
    subject = replace(workshop, starts_at=starts_at, ends_at=starts_at + timedelta(hours=3))
    assert subject.registration_cutoff == expected_cutoff
    assert subject.registration_cutoff.tzinfo == WORKSHOP_TIMEZONE
    assert subject.starts_at.astimezone(UTC) - subject.registration_cutoff.astimezone(UTC) == (
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
    created = datetime(2026, 12, 1, tzinfo=UTC)
    state.workshops.append(workshop)
    state.registrations.extend(
        [
            Registration(
                "registration-1",
                "workshop-1",
                "participant-1",
                RegistrationStatus.CONFIRMED,
                created,
                created,
            ),
            Registration(
                "registration-2",
                "workshop-1",
                "participant-2",
                RegistrationStatus.CANCELLED,
                created,
                created + timedelta(hours=1),
            ),
        ]
    )
    state.next_workshop_id = 2
    state.next_registration_id = 3
    expected = deepcopy(state)
    app.sidebar.button(key="refresh_view").click().run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()

    assert not app.exception
    assert app.session_state.demo_state is state
    assert app.session_state.demo_state == expected
    assert app.metric[0].value == "1"
    assert app.metric[1].value == "1"


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


@pytest.fixture
def populated_state(workshop: Workshop) -> DemoState:
    state = create_demo_state()
    created = datetime(2026, 12, 1, tzinfo=UTC)
    state.workshops.append(workshop)
    state.registrations.extend(
        [
            Registration(
                "registration-1",
                "workshop-1",
                "participant-1",
                RegistrationStatus.CONFIRMED,
                created,
                created,
            ),
            Registration(
                "registration-2",
                "workshop-1",
                "participant-2",
                RegistrationStatus.CANCELLED,
                created,
                created + timedelta(hours=1),
            ),
        ]
    )
    state.next_workshop_id = 2
    state.next_registration_id = 3
    return state


@pytest.mark.parametrize(
    ("user_id", "display_name", "role"),
    [
        ("organiser-1", "Rui Yan", Role.ORGANISER),
        ("organiser-2", "Alex", Role.ORGANISER),
        ("participant-1", "Xingjian", Role.PARTICIPANT),
        ("participant-2", "Sam", Role.PARTICIPANT),
    ],
)
def test_fixed_identity_resolves_by_id_without_mutation(
    populated_state: DemoState, user_id: str, display_name: str, role: Role
) -> None:
    expected = deepcopy(populated_state)
    actor = resolve_actor(populated_state, user_id)
    assert actor == DemoUser(user_id, display_name, role)
    assert actor is next(user for user in populated_state.users if user.user_id == user_id)
    assert populated_state == expected


@pytest.mark.parametrize("user_id", [None, "", "missing-user", "Rui Yan"])
def test_unselected_unknown_and_display_name_inputs_do_not_resolve(
    populated_state: DemoState, user_id: str | None
) -> None:
    expected = deepcopy(populated_state)
    actor = resolve_actor(populated_state, user_id)
    assert actor is None
    assert check_permission(populated_state, actor, Role.ORGANISER) == "INVALID_ACTOR"
    assert populated_state == expected


@pytest.mark.parametrize(
    ("user_id", "required_role", "owner_id", "expected_outcome"),
    [
        ("organiser-1", Role.ORGANISER, None, "OK"),
        ("participant-1", Role.PARTICIPANT, None, "OK"),
        ("participant-1", Role.ORGANISER, None, "FORBIDDEN"),
        ("organiser-1", Role.PARTICIPANT, None, "FORBIDDEN"),
        ("organiser-1", Role.ORGANISER, "organiser-1", "OK"),
        ("organiser-2", Role.ORGANISER, "organiser-1", "FORBIDDEN"),
        ("participant-1", Role.PARTICIPANT, "participant-1", "OK"),
        ("participant-2", Role.PARTICIPANT, "participant-1", "FORBIDDEN"),
    ],
)
def test_role_and_owner_checks_return_explicit_outcomes_without_mutation(
    populated_state: DemoState,
    user_id: str,
    required_role: Role,
    owner_id: str | None,
    expected_outcome: str,
) -> None:
    expected = deepcopy(populated_state)
    actor = resolve_actor(populated_state, user_id)
    assert (
        check_permission(populated_state, actor, required_role, owner_id=owner_id)
        == expected_outcome
    )
    assert populated_state == expected


@pytest.mark.parametrize(
    "actor",
    [
        DemoUser("organiser-1", "Rui Yan", Role.PARTICIPANT),
        DemoUser("participant-1", "Xingjian", Role.ORGANISER),
        DemoUser("missing-user", "Rui Yan", Role.ORGANISER),
    ],
)
def test_unknown_or_role_inconsistent_actor_is_invalid(
    populated_state: DemoState, actor: DemoUser
) -> None:
    expected = deepcopy(populated_state)
    assert (
        check_permission(populated_state, actor, Role.ORGANISER, owner_id="organiser-1")
        == "INVALID_ACTOR"
    )
    assert populated_state == expected


def test_equal_display_names_do_not_grant_another_organisers_permission(
    populated_state: DemoState,
) -> None:
    populated_state.users = [
        replace(user, display_name="Shared name") if user.role == Role.ORGANISER else user
        for user in populated_state.users
    ]
    expected = deepcopy(populated_state)
    actor = resolve_actor(populated_state, "organiser-2")
    assert (
        check_permission(populated_state, actor, Role.ORGANISER, owner_id="organiser-1")
        == "FORBIDDEN"
    )
    assert populated_state == expected


def test_identity_selector_has_only_the_fixed_demo_options() -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert not app.exception
    assert len(app.sidebar.selectbox) == 1
    assert app.sidebar.selectbox(key="selected_user_id").options == [
        "No demo identity selected",
        "Xingjian (PARTICIPANT)",
        "Sam (PARTICIPANT)",
        "Rui Yan (ORGANISER)",
        "Alex (ORGANISER)",
    ]
    assert any("not secure login" in item.value for item in app.sidebar.caption)


@pytest.mark.parametrize(
    ("user_id", "display_name", "role"),
    [
        ("organiser-1", "Rui Yan", Role.ORGANISER),
        ("organiser-2", "Alex", Role.ORGANISER),
        ("participant-1", "Xingjian", Role.PARTICIPANT),
        ("participant-2", "Sam", Role.PARTICIPANT),
    ],
)
def test_selected_fixed_role_controls_both_restricted_preview_views(
    user_id: str, display_name: str, role: Role
) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
    assert f"Selected: {display_name} | Role: {role}" in [
        item.value for item in app.sidebar.caption
    ]
    for view, required_role in [("My Bookings", Role.PARTICIPANT), ("Organiser", Role.ORGANISER)]:
        app.sidebar.radio(key="current_view").set_value(view).run()
        assert not app.exception
        if role == required_role:
            assert not app.warning
            assert not app.error
            expected_message = (
                "Booking actions and personal history will be added in later loops."
                if view == "My Bookings"
                else "Workshop creation and organiser rosters are not yet available."
            )
            assert expected_message in [item.value for item in app.info]
        else:
            assert [item.value for item in app.warning] == [
                f"This view is available to {required_role.value.lower()}s only."
            ]


def test_identity_switch_clear_refresh_and_navigation_preserve_complete_state(
    populated_state: DemoState,
) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.session_state.demo_state = populated_state
    expected = deepcopy(populated_state)
    for user_id in ["organiser-1", "participant-1", "organiser-2", "participant-2", None]:
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        for view in ["Workshops", "My Bookings", "Organiser"]:
            app.sidebar.radio(key="current_view").set_value(view).run()
            app.sidebar.button(key="refresh_view").click().run()
            assert not app.exception
            assert app.session_state.demo_state is populated_state
            assert app.session_state.demo_state == expected
            assert [metric.value for metric in app.metric] == ["1", "1"]
    assert app.sidebar.selectbox(key="selected_user_id").value is None


@pytest.mark.parametrize("view", ["My Bookings", "Organiser"])
def test_unselected_identity_cannot_use_restricted_preview(view: str) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.sidebar.radio(key="current_view").set_value(view).run()
    assert not app.exception
    assert [item.value for item in app.warning] == ["Select a demo identity to use this view."]


def test_separate_sessions_do_not_share_selected_identity() -> None:
    first = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    second = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    first.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    second.run()
    assert second.sidebar.selectbox(key="selected_user_id").value is None
    second.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    first.run()
    assert not first.exception and not second.exception
    assert first.sidebar.selectbox(key="selected_user_id").value == "organiser-1"
    assert second.sidebar.selectbox(key="selected_user_id").value == "participant-1"


@pytest.mark.parametrize(
    ("view", "user_id", "outcome"),
    [("Organiser", "organiser-1", None), ("My Bookings", "participant-1", "UNEXPECTED")],
)
def test_permission_failure_does_not_render_allowed_preview_or_change_state(
    populated_state: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    view: str,
    user_id: str,
    outcome: str | None,
) -> None:
    monkeypatch.setattr("booking.check_permission", lambda *args, **kwargs: outcome)
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.session_state.demo_state = populated_state
    expected = deepcopy(populated_state)
    app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
    app.sidebar.radio(key="current_view").set_value(view).run()

    assert not app.exception
    assert [item.value for item in app.error] == [
        "This view is unavailable. Please refresh and try again."
    ]
    assert all(
        item.value
        not in {
            "Booking actions and personal history will be added in later loops.",
            "Workshop creation and organiser rosters are not yet available.",
        }
        for item in app.info
    )
    assert app.session_state.demo_state is populated_state
    assert app.session_state.demo_state == expected
