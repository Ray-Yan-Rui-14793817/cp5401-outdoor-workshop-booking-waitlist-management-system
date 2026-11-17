"""L1/L2 regressions and L3 workshop, roster and demo-data checks."""

from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from booking import (
    WORKSHOP_TIMEZONE,
    DemoState,
    DemoUser,
    Registration,
    RegistrationStatus,
    Role,
    Workshop,
    browse_workshops,
    check_permission,
    confirmed_count,
    create_demo_data,
    create_demo_state,
    create_workshop,
    get_workshop_roster,
    list_owned_workshops,
    resolve_actor,
)

APP_PATH = Path(__file__).with_name("app.py")
PREVIEW_MESSAGES = {
    "Workshops": "Browse workshops below. Times are shown in Asia/Singapore.",
    "My Bookings": "Booking actions and personal history will be added in later loops.",
    "Organiser": "Create workshops and view confirmed rosters for your own workshops.",
}
NOW = datetime(2026, 12, 1, 9, tzinfo=WORKSHOP_TIMEZONE)
CREATION_REJECTED = (
    "Workshop not created. Your entries have been kept. "
    "Correct the highlighted fields and submit again."
)


def app_with_state(state: DemoState) -> AppTest:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30)
    app.session_state.demo_state = state
    return app.run()


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
    app = app_with_state(create_demo_state())
    if view != "Workshops":
        user_id = "participant-1" if view == "My Bookings" else "organiser-1"
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
    app.sidebar.radio(key="current_view").set_value(view).run()
    assert not app.exception
    assert app.subheader[0].value == view
    assert app.metric[0].value == "0"
    assert app.metric[1].value == "0"


def test_app_refresh_and_navigation_preserve_session_state(workshop: Workshop) -> None:
    app = app_with_state(create_demo_state())
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
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()

    assert not app.exception
    assert app.session_state.demo_state is state
    assert app.session_state.demo_state == expected
    assert app.metric[0].value == "1"
    assert app.metric[1].value == "1"


def test_independent_app_sessions_do_not_share_state(workshop: Workshop) -> None:
    first = app_with_state(create_demo_state())
    second = app_with_state(create_demo_state())
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
def test_fixed_roles_show_only_allowed_menu_and_preview(
    user_id: str, display_name: str, role: Role
) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
    assert f"Selected: {display_name} | Role: {role}" in [
        item.value for item in app.sidebar.caption
    ]
    allowed_view = "My Bookings" if role == Role.PARTICIPANT else "Organiser"
    assert app.sidebar.radio(key="current_view").options == ["Workshops", allowed_view]
    for view in ["Workshops", allowed_view]:
        app.sidebar.radio(key="current_view").set_value(view).run()
        assert not app.exception
        assert not app.warning
        assert not app.error
        assert PREVIEW_MESSAGES[view] in [item.value for item in app.info]


def test_identity_switch_clear_refresh_and_navigation_preserve_complete_state(
    populated_state: DemoState,
) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.session_state.demo_state = populated_state
    expected = deepcopy(populated_state)
    for user_id, views in [
        ("organiser-1", ["Workshops", "Organiser"]),
        ("participant-1", ["Workshops", "My Bookings"]),
        ("organiser-2", ["Workshops", "Organiser"]),
        ("participant-2", ["Workshops", "My Bookings"]),
        (None, ["Workshops"]),
    ]:
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        assert app.sidebar.radio(key="current_view").options == views
        for view in views:
            app.sidebar.radio(key="current_view").set_value(view).run()
            app.sidebar.button(key="refresh_view").click().run()
            assert not app.exception
            assert app.session_state.demo_state is populated_state
            assert app.session_state.demo_state == expected
            assert [metric.value for metric in app.metric] == ["1", "1"]
    assert app.sidebar.selectbox(key="selected_user_id").value is None


def test_unselected_identity_shows_public_preview_and_only_public_menu() -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert not app.exception
    assert app.sidebar.radio(key="current_view").options == ["Workshops"]
    assert app.subheader[0].value == "Workshops"
    assert PREVIEW_MESSAGES["Workshops"] in [item.value for item in app.info]
    assert not app.warning and not app.error


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
    app = app_with_state(populated_state)
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
            PREVIEW_MESSAGES["My Bookings"],
            PREVIEW_MESSAGES["Organiser"],
        }
        for item in app.info
    )
    assert not app.dataframe
    assert all(button.key != "create_workshop" for button in app.button)
    assert app.session_state.demo_state is populated_state
    assert app.session_state.demo_state == expected


@pytest.mark.parametrize(
    ("user_id", "forced_view", "expected_warning"),
    [
        ("participant-1", "Organiser", "This view is available to organisers only."),
        ("organiser-1", "My Bookings", "This view is available to participants only."),
        (None, "Organiser", "Select a demo identity to use this view."),
        (None, "My Bookings", "Select a demo identity to use this view."),
        ("organiser-1", "Unknown view", None),
    ],
)
def test_bypassing_hidden_menu_still_rejects_access_without_mutation(
    populated_state: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    user_id: str | None,
    forced_view: str,
    expected_warning: str | None,
) -> None:
    real_radio = st.radio

    def bypass_menu(*args, **kwargs):
        real_radio(*args, **kwargs)
        return forced_view

    monkeypatch.setattr(st, "radio", bypass_menu)
    app = AppTest.from_file(str(APP_PATH), default_timeout=30)
    app.session_state.demo_state = populated_state
    app.session_state.selected_user_id = user_id
    expected = deepcopy(populated_state)
    app.run()

    assert not app.exception
    assert forced_view not in app.sidebar.radio(key="current_view").options
    if expected_warning is None:
        assert [item.value for item in app.error] == [
            "This view is unavailable. Please refresh and try again."
        ]
    else:
        assert [item.value for item in app.warning] == [expected_warning]
    assert all(
        item.value
        not in {
            PREVIEW_MESSAGES["My Bookings"],
            PREVIEW_MESSAGES["Organiser"],
        }
        for item in app.info
    )
    assert not app.dataframe
    assert all(button.key != "create_workshop" for button in app.button)
    assert app.session_state.demo_state is populated_state
    assert app.session_state.demo_state == expected


@pytest.fixture
def creation_input() -> dict:
    return {
        "title": "  Trail Planning  ",
        "starts_at": NOW + timedelta(hours=48),
        "ends_at": NOW + timedelta(hours=51),
        "location": "  North Trail Meeting Point  ",
        "capacity": 10,
        "preparation_notes": "  Bring water.  ",
        "now": NOW,
    }


@pytest.fixture
def demo_data() -> DemoState:
    return create_demo_data(NOW)


@pytest.mark.parametrize("owner_id", ["organiser-1", "organiser-2"])
@pytest.mark.parametrize("capacity", [1, 30])
def test_create_assigns_id_owner_and_normalised_fields_without_input_mutation(
    populated_state: DemoState, creation_input: dict, owner_id: str, capacity: int
) -> None:
    expected = deepcopy(populated_state)
    outcome, candidate = create_workshop(
        populated_state,
        resolve_actor(populated_state, owner_id),
        **{**creation_input, "capacity": capacity},
    )
    assert outcome == "OK"
    assert candidate is not populated_state
    assert populated_state == expected
    assert candidate.workshops[:-1] == expected.workshops
    created = candidate.workshops[-1]
    assert (created.workshop_id, created.owner_id, created.capacity) == (
        "workshop-2",
        owner_id,
        capacity,
    )
    assert (created.title, created.location, created.preparation_notes) == (
        "Trail Planning",
        "North Trail Meeting Point",
        "Bring water.",
    )
    assert candidate.next_workshop_id == 3
    assert candidate.next_registration_id == expected.next_registration_id
    assert candidate.registrations == expected.registrations
    assert candidate.users == expected.users
    assert candidate.users is not populated_state.users
    assert candidate.workshops is not populated_state.workshops
    assert candidate.registrations is not populated_state.registrations


@pytest.mark.parametrize(
    ("lead", "expected_outcome"),
    [
        (timedelta(hours=24, seconds=1), "OK"),
        (timedelta(hours=24), "INVALID_INPUT"),
        (timedelta(hours=24) - timedelta(seconds=1), "INVALID_INPUT"),
        (timedelta(seconds=-1), "INVALID_INPUT"),
    ],
)
def test_creation_requires_strictly_more_than_twenty_four_hours(
    populated_state: DemoState, creation_input: dict, lead: timedelta, expected_outcome: str
) -> None:
    before = deepcopy(populated_state)
    start = NOW + lead
    outcome, candidate = create_workshop(
        populated_state,
        resolve_actor(populated_state, "organiser-1"),
        **{**creation_input, "starts_at": start, "ends_at": start + timedelta(hours=1)},
    )
    assert outcome == expected_outcome
    assert populated_state == before
    if outcome == "OK":
        assert candidate.next_workshop_id == before.next_workshop_id + 1
    else:
        assert candidate is populated_state
        assert candidate == before


@pytest.mark.parametrize("capacity", [0, -1, 31, 1.5, True, False, "10", None])
def test_creation_rejects_invalid_capacity_without_allocating_an_id(
    populated_state: DemoState, creation_input: dict, capacity: object
) -> None:
    before = deepcopy(populated_state)
    outcome, candidate = create_workshop(
        populated_state,
        resolve_actor(populated_state, "organiser-1"),
        **{**creation_input, "capacity": capacity},
    )
    assert outcome == "INVALID_INPUT"
    assert candidate is populated_state
    assert populated_state == before


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", ""),
        ("title", "  "),
        ("title", None),
        ("location", ""),
        ("location", "  "),
        ("location", None),
        ("preparation_notes", None),
        ("starts_at", None),
        ("starts_at", datetime(2026, 12, 3, 9)),
        ("ends_at", None),
        ("ends_at", datetime(2026, 12, 3, 12)),
        ("now", None),
        ("now", datetime(2026, 12, 1, 9)),
        ("ends_at", NOW + timedelta(hours=48)),
        ("ends_at", NOW + timedelta(hours=47)),
    ],
)
def test_creation_rejects_invalid_fields_and_times_without_mutation(
    populated_state: DemoState, creation_input: dict, field: str, value: object
) -> None:
    before = deepcopy(populated_state)
    outcome, candidate = create_workshop(
        populated_state,
        resolve_actor(populated_state, "organiser-1"),
        **{**creation_input, field: value},
    )
    assert outcome == "INVALID_INPUT"
    assert candidate is populated_state
    assert populated_state == before


@pytest.mark.parametrize(
    ("actor", "expected_outcome"),
    [
        (None, "INVALID_ACTOR"),
        (DemoUser("participant-1", "Xingjian", Role.PARTICIPANT), "FORBIDDEN"),
        (DemoUser("participant-1", "Xingjian", Role.ORGANISER), "INVALID_ACTOR"),
        (DemoUser("missing-user", "Unknown", Role.ORGANISER), "INVALID_ACTOR"),
    ],
)
@pytest.mark.parametrize("capacity", [10, 0])
def test_creation_enforces_actor_and_role_before_invalid_input(
    populated_state: DemoState,
    creation_input: dict,
    actor: DemoUser | None,
    expected_outcome: str,
    capacity: int,
) -> None:
    before = deepcopy(populated_state)
    outcome, candidate = create_workshop(
        populated_state, actor, **{**creation_input, "capacity": capacity}
    )
    assert outcome == expected_outcome
    assert candidate is populated_state
    assert populated_state == before


def test_sequential_creation_uses_returned_state_and_preserves_older_snapshots(
    populated_state: DemoState, creation_input: dict
) -> None:
    actor = resolve_actor(populated_state, "organiser-1")
    creation_input.pop("preparation_notes")
    original = deepcopy(populated_state)
    first_outcome, first = create_workshop(populated_state, actor, **creation_input)
    first_snapshot = deepcopy(first)
    second_outcome, second = create_workshop(first, actor, **creation_input)
    assert first_outcome == second_outcome == "OK"
    assert [w.workshop_id for w in second.workshops] == ["workshop-1", "workshop-2", "workshop-3"]
    assert second.next_workshop_id == 4
    assert second.workshops[-1].preparation_notes == ""
    assert first == first_snapshot
    assert populated_state == original


def test_creation_exception_preserves_all_input_records_and_counters(
    populated_state: DemoState, creation_input: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = deepcopy(populated_state)

    def fail_construction(*args, **kwargs):
        raise RuntimeError("Injected construction failure")

    monkeypatch.setattr("booking.Workshop", fail_construction)
    with pytest.raises(RuntimeError, match="Injected construction failure"):
        create_workshop(
            populated_state, resolve_actor(populated_state, "organiser-1"), **creation_input
        )
    assert populated_state == before


def test_public_browse_orders_instants_and_counts_only_matching_confirmed_records(
    populated_state: DemoState, workshop: Workshop
) -> None:
    other = replace(
        workshop, workshop_id="workshop-2", starts_at=workshop.starts_at - timedelta(days=1)
    )
    populated_state.workshops.append(other)
    populated_state.registrations.append(
        Registration(
            "registration-3", "workshop-2", "participant-2", RegistrationStatus.CONFIRMED, NOW, NOW
        )
    )
    before = deepcopy(populated_state)
    assert [w.workshop_id for w in browse_workshops(populated_state)] == [
        "workshop-2",
        "workshop-1",
    ]
    assert confirmed_count(populated_state, "workshop-1") == 1
    assert confirmed_count(populated_state, "workshop-2") == 1
    assert confirmed_count(populated_state, "missing") == 0
    assert populated_state == before


@pytest.mark.parametrize(
    ("user_id", "expected_outcome", "expected_ids"),
    [
        ("organiser-1", "OK", {"workshop-1", "workshop-3"}),
        ("organiser-2", "OK", {"workshop-2", "workshop-4"}),
        ("participant-1", "FORBIDDEN", set()),
        (None, "INVALID_ACTOR", set()),
    ],
)
def test_owned_workshop_list_enforces_role_and_filters_by_id_without_mutation(
    demo_data: DemoState, user_id: str | None, expected_outcome: str, expected_ids: set[str]
) -> None:
    before = deepcopy(demo_data)
    outcome, workshops = list_owned_workshops(demo_data, resolve_actor(demo_data, user_id))
    assert outcome == expected_outcome
    assert {w.workshop_id for w in workshops} == expected_ids
    assert demo_data == before


@pytest.mark.parametrize(
    ("user_id", "target", "expected_outcome", "expected_ids"),
    [
        ("organiser-1", "workshop-1", "OK", ["registration-1"]),
        ("organiser-1", "workshop-3", "OK", ["registration-3"]),
        ("organiser-2", "workshop-2", "OK", ["registration-2"]),
        ("organiser-2", "workshop-4", "OK", []),
        ("organiser-1", "workshop-2", "FORBIDDEN", []),
        ("organiser-2", "workshop-1", "FORBIDDEN", []),
        ("participant-1", "workshop-1", "FORBIDDEN", []),
        (None, "workshop-1", "INVALID_ACTOR", []),
        ("organiser-1", "missing-workshop", "UNKNOWN_WORKSHOP", []),
        ("participant-1", "missing-workshop", "FORBIDDEN", []),
    ],
)
def test_roster_checks_actual_target_owner_and_returns_no_records_on_denial(
    demo_data: DemoState,
    user_id: str | None,
    target: str,
    expected_outcome: str,
    expected_ids: list[str],
) -> None:
    before = deepcopy(demo_data)
    outcome, records = get_workshop_roster(demo_data, resolve_actor(demo_data, user_id), target)
    assert outcome == expected_outcome
    assert [row.registration_id for row in records] == expected_ids
    assert all(row.status == RegistrationStatus.CONFIRMED for row in records)
    assert demo_data == before


def test_roster_does_not_trust_a_previous_owner_selection(demo_data: DemoState) -> None:
    demo_data.workshops[0] = replace(demo_data.workshops[0], owner_id="organiser-2")
    before = deepcopy(demo_data)
    outcome, records = get_workshop_roster(
        demo_data, resolve_actor(demo_data, "organiser-1"), "workshop-1"
    )
    assert outcome == "FORBIDDEN"
    assert records == ()
    assert demo_data == before


@pytest.mark.parametrize(
    ("now", "start", "expected_outcome"),
    [
        (
            datetime(2026, 10, 31, 9, tzinfo=ZoneInfo("America/New_York")),
            datetime(2026, 11, 1, 9, tzinfo=ZoneInfo("America/New_York")),
            "OK",
        ),
        (
            datetime(2026, 3, 7, 9, tzinfo=ZoneInfo("America/New_York")),
            datetime(2026, 3, 8, 9, tzinfo=ZoneInfo("America/New_York")),
            "INVALID_INPUT",
        ),
        (
            datetime(2026, 12, 1, 1, tzinfo=UTC),
            datetime(2026, 12, 2, 9, tzinfo=WORKSHOP_TIMEZONE),
            "INVALID_INPUT",
        ),
    ],
)
def test_creation_compares_elapsed_hours_between_aware_instants(
    populated_state: DemoState,
    creation_input: dict,
    now: datetime,
    start: datetime,
    expected_outcome: str,
) -> None:
    before = deepcopy(populated_state)
    outcome, candidate = create_workshop(
        populated_state,
        resolve_actor(populated_state, "organiser-1"),
        **{**creation_input, "now": now, "starts_at": start, "ends_at": start + timedelta(hours=1)},
    )
    assert outcome == expected_outcome
    assert populated_state == before
    if outcome != "OK":
        assert candidate is populated_state


def test_demo_data_has_valid_relative_history_capacity_and_independent_collections(
    demo_data: DemoState,
) -> None:
    second = create_demo_data(NOW)
    assert (len(demo_data.workshops), len(demo_data.registrations)) == (4, 4)
    assert demo_data.next_workshop_id == demo_data.next_registration_id == 5
    users = {user.user_id: user for user in demo_data.users}
    workshops = {workshop.workshop_id: workshop for workshop in demo_data.workshops}
    assert set(workshops) == {f"workshop-{index}" for index in range(1, 5)}
    assert {row.registration_id for row in demo_data.registrations} == {
        f"registration-{index}" for index in range(1, 5)
    }
    for workshop in demo_data.workshops:
        assert users[workshop.owner_id].role == Role.ORGANISER
    for row in demo_data.registrations:
        assert row.workshop_id in workshops
        assert users[row.participant_id].role == Role.PARTICIPANT
    active_pairs = [
        (row.workshop_id, row.participant_id)
        for row in demo_data.registrations
        if row.status == RegistrationStatus.CONFIRMED
    ]
    assert len(active_pairs) == len(set(active_pairs))
    assert demo_data.workshops[0].starts_at - NOW >= timedelta(hours=48)
    assert demo_data.workshops[1].starts_at - NOW >= timedelta(hours=48)
    assert demo_data.workshops[2].registration_cutoff <= NOW < demo_data.workshops[2].starts_at
    assert demo_data.workshops[3].ends_at < NOW
    for workshop in demo_data.workshops:
        assert 0 <= confirmed_count(demo_data, workshop.workshop_id) <= workshop.capacity
        assert workshop.starts_at - (NOW - timedelta(days=7)) > timedelta(hours=24)
        for row in demo_data.registrations:
            if row.workshop_id == workshop.workshop_id:
                assert row.created_at <= row.updated_at < workshop.registration_cutoff
                assert row.updated_at < NOW
    assert confirmed_count(demo_data, "workshop-2") == 1
    assert demo_data.users is not second.users
    assert demo_data.workshops is not second.workshops
    assert demo_data.registrations is not second.registrations


def fill_creation_form(app: AppTest, start: datetime) -> None:
    local = start.astimezone(WORKSHOP_TIMEZONE)
    end = local + timedelta(hours=2)
    app.text_input(key="new_title").set_value("Human Check Workshop")
    app.text_input(key="new_location").set_value("East Trail Entrance")
    app.date_input(key="new_start_date").set_value(local.date())
    app.time_input(key="new_start_time").set_value(local.time())
    app.date_input(key="new_end_date").set_value(end.date())
    app.time_input(key="new_end_time").set_value(end.time())
    app.number_input(key="new_capacity").set_value(1)
    app.text_area(key="new_notes").set_value("Bring water and closed-toe shoes.")


def creation_form_values(app: AppTest) -> dict:
    def date_value(key: str):
        value = app.date_input(key=key).value
        # AppTest stores a pending single-date edit as a tuple until the next run.
        return (value[0] if value else None) if isinstance(value, tuple) else value

    return {
        "title": app.text_input(key="new_title").value,
        "start_date": date_value("new_start_date"),
        "start_time": app.time_input(key="new_start_time").value,
        "end_date": date_value("new_end_date"),
        "end_time": app.time_input(key="new_end_time").value,
        "location": app.text_input(key="new_location").value,
        "capacity": app.number_input(key="new_capacity").value,
        "notes": app.text_area(key="new_notes").value,
    }


@pytest.mark.parametrize(
    ("widget", "key", "invalid", "message"),
    [
        ("text_input", "new_title", "  ", "Title is required."),
        ("text_input", "new_location", "  ", "Meeting point is required."),
        ("time_input", "new_end_time", time(8), "End date and time must be after the start."),
        (
            "date_input",
            "new_start_date",
            (NOW + timedelta(days=1)).date(),
            "Start must be more than 24 hours from submission.",
        ),
        ("number_input", "new_capacity", 0, "Capacity must be a whole number from 1 to 30."),
        ("number_input", "new_capacity", 31, "Capacity must be a whole number from 1 to 30."),
        ("date_input", "new_start_date", None, "Choose a valid start date and time."),
        ("date_input", "new_end_date", None, "Choose a valid end date and time."),
    ],
)
def test_creation_failure_keeps_all_fields_and_identifies_the_error(
    demo_data: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    widget: str,
    key: str,
    invalid: object,
    message: str,
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-2").run()
    app.session_state.review_marker = {"keep": ["human draft"]}
    fill_creation_form(app, NOW + timedelta(hours=48))
    getattr(app, widget)(key=key).set_value(invalid)
    expected_fields = creation_form_values(app)
    before = deepcopy(demo_data)

    app.button(key="create_workshop").click().run()

    assert not app.exception and not app.success
    assert [item.value for item in app.error] == [CREATION_REJECTED, message]
    assert creation_form_values(app) == expected_fields
    assert app.session_state.demo_state is demo_data
    assert demo_data == before
    assert app.sidebar.selectbox(key="selected_user_id").value == "organiser-2"
    assert app.sidebar.radio(key="current_view").value == "Organiser"
    assert app.selectbox(key="roster_workshop_id").value == "workshop-2"
    assert app.session_state.review_marker == {"keep": ["human draft"]}


@pytest.mark.parametrize("owner_id", ["organiser-1", "organiser-2"])
def test_corrected_creation_adds_one_workshop_and_resets_only_the_form(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, owner_id: str
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value(owner_id).run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.session_state.review_marker = {"keep": ["human draft"]}
    before = deepcopy(demo_data)
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_location").set_value("  ")
    app.button(key="create_workshop").click().run()
    assert "Meeting point is required." in [item.value for item in app.error]
    assert demo_data == before

    app.text_input(key="new_location").set_value("  East Trail Entrance  ")
    app.button(key="create_workshop").click().run()

    assert not app.exception and not app.error
    candidate = app.session_state.demo_state
    assert len(candidate.workshops) == len(before.workshops) + 1
    assert candidate.workshops[:-1] == before.workshops
    created = candidate.workshops[-1]
    assert (created.workshop_id, created.owner_id, created.title, created.location) == (
        "workshop-5",
        owner_id,
        "Human Check Workshop",
        "East Trail Entrance",
    )
    assert created.starts_at == NOW + timedelta(hours=48)
    assert created.capacity == 1
    assert created.preparation_notes == "Bring water and closed-toe shoes."
    assert candidate.next_workshop_id == before.next_workshop_id + 1
    assert candidate.next_registration_id == before.next_registration_id
    assert candidate.registrations == before.registrations
    assert candidate.users == before.users
    assert demo_data == before
    assert [item.value for item in app.success] == ["Created workshop-5: Human Check Workshop."]
    assert creation_form_values(app) == {
        "title": "",
        "start_date": (NOW + timedelta(days=3)).date(),
        "start_time": time(9),
        "end_date": (NOW + timedelta(days=3)).date(),
        "end_time": time(12),
        "location": "",
        "capacity": 10,
        "notes": "",
    }
    assert app.sidebar.selectbox(key="selected_user_id").value == owner_id
    assert app.sidebar.radio(key="current_view").value == "Organiser"
    assert app.selectbox(key="roster_workshop_id").value == "workshop-5"
    assert app.session_state.review_marker == {"keep": ["human draft"]}

    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.success
    assert app.session_state.demo_state is candidate
    assert len(candidate.workshops) == 5 and candidate.next_workshop_id == 6


def test_creation_shows_all_field_errors_without_discarding_invalid_values(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=24))
    app.text_input(key="new_title").set_value("")
    app.text_input(key="new_location").set_value("  ")
    app.number_input(key="new_capacity").set_value(31)
    app.time_input(key="new_end_time").set_value(time(8))
    expected_fields = creation_form_values(app)
    before = deepcopy(demo_data)
    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.success
    assert {
        "Title is required.",
        "Meeting point is required.",
        "Capacity must be a whole number from 1 to 30.",
        "Start must be more than 24 hours from submission.",
        "End date and time must be after the start.",
        CREATION_REJECTED,
    } == {item.value for item in app.error}
    assert len(app.error) == 6
    assert creation_form_values(app) == expected_fields
    assert app.session_state.demo_state is demo_data and demo_data == before


@pytest.mark.parametrize("route", ["public", "role-switch"])
def test_failed_creation_survives_leaving_the_form_and_retry_uses_current_owner(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, route: str
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.session_state.review_marker = {"keep": ["human draft"]}
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_location").set_value("  ")
    app.button(key="create_workshop").click().run()
    failed_values = creation_form_values(app)
    before = deepcopy(demo_data)

    if route == "public":
        app.sidebar.radio(key="current_view").set_value("Workshops").run()
        app.sidebar.button(key="refresh_view").click().run()
        expected_owner = "organiser-1"
    else:
        app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
        app.sidebar.radio(key="current_view").set_value("My Bookings").run()
        app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
        expected_owner = "organiser-2"
    app.sidebar.radio(key="current_view").set_value("Organiser").run()

    assert not app.exception and not app.warning
    assert creation_form_values(app) == failed_values
    assert [item.value for item in app.error] == [CREATION_REJECTED, "Meeting point is required."]
    assert app.session_state.demo_state is demo_data and demo_data == before
    assert app.sidebar.selectbox(key="selected_user_id").value == expected_owner
    assert app.session_state.review_marker == {"keep": ["human draft"]}

    app.text_input(key="new_location").set_value("East Trail Entrance")
    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.error
    candidate = app.session_state.demo_state
    assert candidate.workshops[:-1] == before.workshops
    assert len(candidate.workshops) == 5 and candidate.next_workshop_id == 6
    assert candidate.workshops[-1].owner_id == expected_owner
    assert candidate.workshops[-1].title == "Human Check Workshop"
    assert candidate.registrations == before.registrations
    assert candidate.users == before.users
    assert candidate.next_registration_id == before.next_registration_id
    assert demo_data == before

    reset_values = creation_form_values(app)
    assert (reset_values["title"], reset_values["location"], reset_values["notes"]) == ("", "", "")
    assert reset_values["capacity"] == 10
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    assert not app.exception and not app.error
    assert creation_form_values(app) == reset_values
    assert app.session_state.demo_state is candidate
    assert len(candidate.workshops) == 5 and candidate.next_workshop_id == 6


@pytest.mark.parametrize(
    ("widget", "key", "invalid", "corrected", "message"),
    [
        ("number_input", "new_capacity", 31, 1, "Capacity must be a whole number from 1 to 30."),
        (
            "time_input",
            "new_end_time",
            time(8),
            time(11),
            "End date and time must be after the start.",
        ),
    ],
)
def test_retry_replaces_previous_errors_and_allocates_only_after_correction(
    demo_data: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    widget: str,
    key: str,
    invalid: object,
    corrected: object,
    message: str,
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_location").set_value("")
    before = deepcopy(demo_data)
    app.button(key="create_workshop").click().run()
    assert [item.value for item in app.error] == [CREATION_REJECTED, "Meeting point is required."]

    app.text_input(key="new_location").set_value("East Trail Entrance")
    getattr(app, widget)(key=key).set_value(invalid)
    retry_values = creation_form_values(app)
    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.success
    assert [item.value for item in app.error] == [CREATION_REJECTED, message]
    assert creation_form_values(app) == retry_values
    assert app.session_state.demo_state is demo_data and demo_data == before

    getattr(app, widget)(key=key).set_value(corrected)
    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.error
    candidate = app.session_state.demo_state
    assert len(candidate.workshops) == 5 and candidate.next_workshop_id == 6
    assert candidate.workshops[:-1] == before.workshops
    assert candidate.workshops[-1].owner_id == "organiser-2"
    assert candidate.registrations == before.registrations
    assert candidate.users == before.users
    assert candidate.next_registration_id == before.next_registration_id
    assert demo_data == before


def test_creation_feedback_uses_the_attempt_time_when_the_clock_advances(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    clock = {"now": NOW}
    monkeypatch.setattr("booking.server_now", lambda: clock["now"])

    def create_then_advance(*args, **kwargs):
        result = create_workshop(*args, **kwargs)
        clock["now"] += timedelta(hours=2)
        return result

    monkeypatch.setattr("booking.create_workshop", create_then_advance)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=25))
    app.number_input(key="new_capacity").set_value(31)
    expected_fields = creation_form_values(app)
    before = deepcopy(demo_data)
    app.button(key="create_workshop").click().run()

    assert not app.exception and not app.success
    assert clock["now"] == NOW + timedelta(hours=2)
    assert [item.value for item in app.error] == [
        CREATION_REJECTED,
        "Capacity must be a whole number from 1 to 30.",
    ]
    assert creation_form_values(app) == expected_fields
    assert app.session_state.demo_state is demo_data and demo_data == before


def test_app_seeds_once_and_refresh_uses_current_time_without_reseeding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": NOW}
    monkeypatch.setattr("booking.server_now", lambda: clock["now"])
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    state = app.session_state.demo_state
    before = deepcopy(state)
    assert [m.value for m in app.metric] == ["4", "3"]
    assert any("Registration window open" in row.value for row in app.caption)
    clock["now"] = NOW + timedelta(days=10)
    app.sidebar.button(key="refresh_view").click().run()
    assert not app.exception
    assert app.session_state.demo_state is state
    assert state == before
    assert not any("Registration window open" in row.value for row in app.caption)


def test_ui_creates_for_current_identity_then_browse_and_refresh_preserve_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(create_demo_state())
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.button(key="create_workshop").click().run()
    assert not app.exception
    assert not app.error
    state = app.session_state.demo_state
    assert len(state.workshops) == 1
    assert state.workshops[0].owner_id == "organiser-2"
    assert state.workshops[0].title == "Human Check Workshop"
    assert state.workshops[0].capacity == 1
    assert app.metric[0].value == "1"
    assert any("Created workshop-1" in row.value for row in app.success)
    before = deepcopy(state)
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    app.sidebar.button(key="refresh_view").click().run()
    assert app.session_state.demo_state is state
    assert state == before
    assert any("Human Check Workshop" in row.value for row in app.markdown)


def test_creation_form_checks_fresh_submission_time_and_preserves_rejection_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": NOW}
    monkeypatch.setattr("booking.server_now", lambda: clock["now"])
    app = app_with_state(create_demo_state())
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=25))
    state = app.session_state.demo_state
    before = deepcopy(state)
    clock["now"] = NOW + timedelta(hours=2)
    app.button(key="create_workshop").click().run()
    assert not app.exception
    assert any("Your entries have been kept" in row.value for row in app.error)
    assert not app.success
    assert app.session_state.demo_state is state
    assert state == before


def test_organiser_identity_switch_resets_roster_to_owned_target(demo_data: DemoState) -> None:
    app = app_with_state(demo_data)
    before = deepcopy(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-1").run()
    assert app.dataframe[0].value["Participant"].tolist() == ["Xingjian"]
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    assert not app.exception
    assert set(app.selectbox(key="roster_workshop_id").options) == {
        "Outdoor Photography Walk (workshop-2)",
        "Past Nature Walk (workshop-4)",
    }
    app.selectbox(key="roster_workshop_id").set_value("workshop-2").run()
    assert app.dataframe[0].value["Participant"].tolist() == ["Sam"]
    assert demo_data == before


@pytest.mark.parametrize(
    ("owner_id", "workshop_id", "expected_count"),
    [
        ("organiser-1", "workshop-1", 1),
        ("organiser-2", "workshop-2", 1),
        ("organiser-2", "workshop-4", 0),
    ],
)
def test_owned_roster_displays_selected_confirmed_count(
    demo_data: DemoState, owner_id: str, workshop_id: str, expected_count: int
) -> None:
    app = app_with_state(demo_data)
    before = deepcopy(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value(owner_id).run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value(workshop_id).run()

    assert not app.exception
    assert f"Confirmed participants: {expected_count}" in [row.value for row in app.caption]
    if expected_count:
        assert len(app.dataframe[0].value) == expected_count
    else:
        assert not app.dataframe
        assert "No confirmed participants for this workshop." in [row.value for row in app.markdown]
    assert demo_data == before


def test_forced_foreign_roster_selection_is_denied_without_disclosure(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_selectbox = st.selectbox

    def force_foreign_target(*args, **kwargs):
        selected = real_selectbox(*args, **kwargs)
        return "workshop-2" if kwargs.get("key") == "roster_workshop_id" else selected

    monkeypatch.setattr(st, "selectbox", force_foreign_target)
    app = app_with_state(demo_data)
    before = deepcopy(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    assert not app.exception
    assert any("FORBIDDEN" in row.value for row in app.error)
    assert not app.dataframe
    assert demo_data == before


def test_public_view_shows_full_details_counts_and_closed_policy(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(demo_data)
    rendered = "\n".join(item.value for item in app.markdown)
    for expected in [
        "Outdoor Navigation Basics",
        "North Trail Meeting Point",
        "2026-12-04 09:00:00 (Asia/Singapore)",
        "2026-12-03 09:00:00 (Asia/Singapore)",
        "Registration cutoff:",
        "Capacity: 10 | Confirmed: 1 | Remaining: 9",
        "Capacity: 1 | Confirmed: 1 | Remaining: 0",
        "Bring water",
    ]:
        assert expected in rendered
    assert any("Confirmed roster locked" in item.value for item in app.caption)
    assert any("Started - historical" in item.value for item in app.caption)
    assert not app.dataframe
    assert not app.exception


@pytest.mark.parametrize("key", ["new_start_date", "new_end_date"])
def test_cleared_creation_date_is_rejected_without_crashing(
    monkeypatch: pytest.MonkeyPatch, key: str
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(create_demo_state())
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.date_input(key=key).set_value(None)
    state = app.session_state.demo_state
    before = deepcopy(state)
    app.button(key="create_workshop").click().run()
    assert not app.exception
    assert any("Your entries have been kept" in item.value for item in app.error)
    assert app.session_state.demo_state is state
    assert state == before


@pytest.mark.parametrize("key", ["new_start_time", "new_end_time"])
def test_missing_time_at_ui_boundary_is_rejected_without_mutation(
    monkeypatch: pytest.MonkeyPatch, key: str
) -> None:
    monkeypatch.setattr("booking.server_now", lambda: NOW)
    app = app_with_state(create_demo_state())
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    real_time_input = st.time_input

    def missing_time(*args, **kwargs):
        value = real_time_input(*args, **kwargs)
        return None if kwargs.get("key") == key else value

    monkeypatch.setattr(st, "time_input", missing_time)
    state = app.session_state.demo_state
    before = deepcopy(state)
    app.button(key="create_workshop").click().run()
    assert not app.exception
    assert any("Your entries have been kept" in item.value for item in app.error)
    assert app.session_state.demo_state is state
    assert state == before


@pytest.mark.parametrize(
    ("first_id", "first_view", "next_id", "expected_view"),
    [
        ("organiser-1", "Organiser", "participant-1", "Workshops"),
        ("participant-1", "My Bookings", "organiser-1", "Workshops"),
        ("organiser-1", "Organiser", None, "Workshops"),
        ("participant-1", "My Bookings", None, "Workshops"),
        ("organiser-1", "Organiser", "organiser-2", "Organiser"),
        ("participant-1", "My Bookings", "participant-2", "My Bookings"),
        ("organiser-1", "Workshops", "participant-1", "Workshops"),
        ("participant-1", "Workshops", "organiser-1", "Workshops"),
    ],
)
def test_identity_change_resets_only_disallowed_current_view(
    populated_state: DemoState,
    first_id: str,
    first_view: str,
    next_id: str | None,
    expected_view: str,
) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30)
    app.session_state.demo_state = populated_state
    expected = deepcopy(populated_state)
    app.run()
    app.sidebar.selectbox(key="selected_user_id").set_value(first_id).run()
    app.sidebar.radio(key="current_view").set_value(first_view).run()
    assert not app.exception
    assert app.sidebar.radio(key="current_view").value == first_view
    assert app.subheader[0].value == first_view
    assert PREVIEW_MESSAGES[first_view] in [item.value for item in app.info]
    assert app.session_state.demo_state is populated_state
    assert app.session_state.demo_state == expected
    app.sidebar.selectbox(key="selected_user_id").set_value(next_id).run()

    assert not app.exception
    assert app.sidebar.radio(key="current_view").value == expected_view
    assert app.subheader[0].value == expected_view
    assert PREVIEW_MESSAGES[expected_view] in [item.value for item in app.info]
    assert not app.warning and not app.error
    assert app.session_state.demo_state is populated_state
    assert app.session_state.demo_state == expected


@pytest.mark.parametrize("stale_view", ["Organiser", "Unknown view"])
def test_stale_or_unknown_saved_view_resets_before_widget_creation(
    populated_state: DemoState, stale_view: str
) -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30)
    app.session_state.demo_state = populated_state
    app.session_state.selected_user_id = "participant-1"
    app.session_state.current_view = stale_view
    expected = deepcopy(populated_state)
    app.run()

    assert not app.exception
    assert app.sidebar.radio(key="current_view").options == ["Workshops", "My Bookings"]
    assert app.sidebar.radio(key="current_view").value == "Workshops"
    assert app.subheader[0].value == "Workshops"
    assert PREVIEW_MESSAGES["Workshops"] in [item.value for item in app.info]
    assert not app.warning and not app.error
    assert app.session_state.demo_state is populated_state
    assert app.session_state.demo_state == expected
