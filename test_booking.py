"""Retained L1-L4 regressions and L5 owned cancellation/history checks."""

from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

import booking
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
    "My Bookings": "View confirmed bookings, waiting entries and history for the selected demo identity.",
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


def rendered_workshop(app: AppTest, workshop_id: str):
    return next(
        card for card in app.get("flex_container") if card.key == f"workshop_card_{workshop_id}"
    )


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

    assert len(second.users) == 6
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
        "participant-leo",
        "participant-willy",
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
        "Leo (PARTICIPANT)",
        "Willy (PARTICIPANT)",
        "Rui Yan (ORGANISER)",
        "Alex (ORGANISER)",
    ]
    assert any(
        "Demo identity selection is not secure authentication." in item.value
        for item in app.main.get("caption")
    )


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
    assert any(
        item.value.endswith(f"[Fictional identity: {display_name} | Role: {role}]")
        for item in app.main.get("markdown")
    )
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


@pytest.mark.parametrize("route", ["direct", "participant", "cleared"])
def test_l4_f08_failed_drafts_and_errors_are_isolated_by_organiser_id(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, route: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    defaults = creation_form_values(app)
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_title").set_value("Rui navigation draft")
    app.text_input(key="new_location").set_value("")
    app.number_input(key="new_capacity").set_value(2)
    app.text_area(key="new_notes").set_value("Rui: bring water.")
    app.button(key="create_workshop").click().run()
    rui_values = creation_form_values(app)
    assert {e.value for e in app.error} == {CREATION_REJECTED, "Meeting point is required."}
    assert app.session_state.demo_state is demo_data and demo_data == before

    if route != "direct":
        user_id = "participant-1" if route == "participant" else None
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        assert "Organiser" not in app.sidebar.radio(key="current_view").options
        assert not app.text_input and not app.error
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    assert creation_form_values(app) == defaults
    assert not app.error and not app.success
    fill_creation_form(app, NOW + timedelta(hours=72))
    app.text_input(key="new_title").set_value("")
    app.text_input(key="new_location").set_value("Alex lakeside shelter")
    app.number_input(key="new_capacity").set_value(31)
    app.text_area(key="new_notes").set_value("Alex: bring a camera.")
    app.button(key="create_workshop").click().run()
    alex_values = creation_form_values(app)
    alex_errors = {
        CREATION_REJECTED,
        "Title is required.",
        "Capacity must be a whole number from 1 to 30.",
    }
    assert {e.value for e in app.error} == alex_errors
    assert app.session_state.demo_state is demo_data and demo_data == before

    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    assert creation_form_values(app) == rui_values
    assert {e.value for e in app.error} == {CREATION_REJECTED, "Meeting point is required."}
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    assert creation_form_values(app) == alex_values
    assert {e.value for e in app.error} == alex_errors
    forms = app.session_state.creation_forms
    assert set(forms) == {"organiser-1", "organiser-2"}
    assert forms["organiser-1"] is not forms["organiser-2"]
    assert len(forms["organiser-1"]["draft"]) == len(forms["organiser-2"]["draft"]) == 8
    assert forms["organiser-1"]["errors"] == {"location": "Meeting point is required."}
    assert forms["organiser-2"]["errors"] == {
        "title": "Title is required.",
        "capacity": "Capacity must be a whole number from 1 to 30.",
    }
    assert all(f["feedback"] == CREATION_REJECTED for f in forms.values())
    assert not app.exception and demo_data == before


@pytest.mark.parametrize("owner_id", ["organiser-1", "organiser-2"])
def test_l4_f08_success_clears_only_the_current_organisers_failed_form(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, owner_id: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    for user_id in ["organiser-1", "organiser-2"]:
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        app.sidebar.radio(key="current_view").set_value("Organiser").run()
        fill_creation_form(app, NOW + timedelta(hours=48))
        app.text_input(key="new_title").set_value(f"Draft for {user_id}")
        app.text_input(key="new_location").set_value("")
        app.button(key="create_workshop").click().run()
    other_id = "organiser-2" if owner_id == "organiser-1" else "organiser-1"
    other_before = deepcopy(app.session_state.creation_forms[other_id])
    app.sidebar.selectbox(key="selected_user_id").set_value(owner_id).run()
    app.text_input(key="new_location").set_value("East trail entrance")
    app.button(key="create_workshop").click().run()
    candidate = app.session_state.demo_state
    assert not app.exception and not app.error and app.success
    assert candidate.workshops[:-1] == before.workshops
    assert candidate.workshops[-1].owner_id == owner_id
    assert candidate.workshops[-1].workshop_id == "workshop-5"
    assert candidate.next_workshop_id == before.next_workshop_id + 1
    assert candidate.registrations == before.registrations
    assert candidate.next_registration_id == before.next_registration_id
    assert candidate.users == before.users and demo_data == before
    assert app.session_state.selected_user_id == owner_id
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
    assert not app.session_state.creation_forms[owner_id].get("draft")
    assert not app.session_state.creation_forms[owner_id].get("errors")
    assert not app.session_state.creation_forms[owner_id].get("feedback")
    assert app.session_state.creation_forms[other_id] == other_before
    app.sidebar.selectbox(key="selected_user_id").set_value(other_id).run()
    assert app.text_input(key="new_title").value == f"Draft for {other_id}"
    assert app.text_input(key="new_location").value == ""
    assert {e.value for e in app.error} == {CREATION_REJECTED, "Meeting point is required."}
    assert not app.success
    app.sidebar.selectbox(key="selected_user_id").set_value(owner_id).run()
    assert app.text_input(key="new_title").value == "" and not app.error
    assert app.session_state.demo_state is candidate


@pytest.mark.parametrize("owner_id", ["organiser-1", "organiser-2"])
def test_l4_f08_draft_identity_fields_cannot_assign_workshop_ownership(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, owner_id: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value(owner_id).run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_location").set_value("")
    app.button(key="create_workshop").click().run()
    other_id = "organiser-2" if owner_id == "organiser-1" else "organiser-1"
    draft = app.session_state.creation_forms[owner_id]["draft"]
    draft.update({"owner_id": other_id, "selected_user_id": other_id, "new_owner_id": other_id})
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    assert app.session_state.selected_user_id == owner_id
    app.text_input(key="new_location").set_value("North trail shelter")
    app.button(key="create_workshop").click().run()
    candidate = app.session_state.demo_state
    assert not app.exception and not app.error and app.success
    assert candidate.workshops[-1].owner_id == owner_id
    assert candidate.workshops[:-1] == before.workshops
    assert candidate.next_workshop_id == before.next_workshop_id + 1
    assert candidate.next_registration_id == before.next_registration_id
    assert candidate.registrations == before.registrations and demo_data == before


def test_l4_f08_latest_failure_replaces_only_its_own_values_and_errors(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_location").set_value("")
    app.button(key="create_workshop").click().run()
    app.text_input(key="new_title").set_value("Latest Rui draft")
    app.text_input(key="new_location").set_value("Rui shelter")
    app.number_input(key="new_capacity").set_value(31)
    app.button(key="create_workshop").click().run()
    latest_values = creation_form_values(app)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    fill_creation_form(app, NOW + timedelta(hours=72))
    app.text_input(key="new_title").set_value("")
    app.button(key="create_workshop").click().run()
    alex_before = deepcopy(app.session_state.creation_forms["organiser-2"])
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    assert creation_form_values(app) == latest_values
    assert {e.value for e in app.error} == {
        CREATION_REJECTED,
        "Capacity must be a whole number from 1 to 30.",
    }
    assert app.session_state.creation_forms["organiser-2"] == alex_before
    assert app.session_state.demo_state is demo_data and demo_data == before
    assert not app.exception


def test_l4_f08_unsubmitted_edits_are_not_shown_to_a_different_organiser(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    defaults = creation_form_values(app)
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_title").set_value("Unsubmitted Rui edits")
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    assert creation_form_values(app) == defaults
    assert not app.error and not app.success and not app.exception
    assert not app.session_state.creation_forms["organiser-1"].get("draft")
    assert app.session_state.demo_state is demo_data and demo_data == before


def test_l4_f08_feedback_is_scoped_even_when_failure_outcomes_differ(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    original_create = booking.create_workshop

    def reject_rui(state: DemoState, actor: DemoUser, **fields: object):
        if actor.user_id == "organiser-1":
            return "FORBIDDEN", state
        return original_create(state, actor, **fields)

    monkeypatch.setattr(booking, "create_workshop", reject_rui)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.button(key="create_workshop").click().run()
    rui_feedback = [e.value for e in app.error]
    assert rui_feedback == ["FORBIDDEN: Only organisers may create workshops."]
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    assert not app.error
    fill_creation_form(app, NOW + timedelta(hours=72))
    app.text_input(key="new_location").set_value("")
    app.button(key="create_workshop").click().run()
    assert {e.value for e in app.error} == {CREATION_REJECTED, "Meeting point is required."}
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    assert [e.value for e in app.error] == rui_feedback
    assert app.session_state.creation_forms["organiser-1"]["errors"] == {}
    assert app.session_state.demo_state is demo_data and demo_data == before
    assert not app.exception and not app.success


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
        app.sidebar.radio(key="current_view").set_value("Organiser").run()
        assert app.text_input(key="new_title").value == ""
        assert not app.error
        app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
        expected_owner = "organiser-1"
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
    open_badges = [item.value for item in app.markdown if item.value.endswith(" OPEN]")]
    assert open_badges == [":green-badge[BOOKING OPEN]", ":orange-badge[FULL / WAITLIST OPEN]"]
    clock["now"] = NOW + timedelta(days=10)
    app.sidebar.button(key="refresh_view").click().run()
    assert not app.exception
    assert app.session_state.demo_state is state
    assert state == before
    assert not any(item.value.endswith(" OPEN]") for item in app.markdown)
    assert sum(item.value.endswith("[STARTED]") for item in app.markdown) == 4


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
    assert f"Confirmed bookings: {expected_count}" in [row.value for row in app.caption]
    if expected_count:
        assert len(app.dataframe[0].value) == expected_count
    else:
        assert not app.dataframe
        assert "No confirmed bookings for this workshop." in [row.value for row in app.markdown]
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
    navigation = rendered_workshop(app, "workshop-1")
    photography = rendered_workshop(app, "workshop-2")
    rendered = "\n".join(item.value for item in navigation.get("markdown"))
    for expected in [
        "Outdoor Navigation Basics",
        "North Trail Meeting Point",
        "Start (S):",
        "2026-12-04 09:00:00 (Asia/Singapore)",
        "2026-12-03 09:00:00 (Asia/Singapore)",
        "Registration cutoff (C):",
        "Remaining places: 9",
        "Bring water",
    ]:
        assert expected in rendered
    assert "Capacity: 10 | Confirmed bookings: 1" in [m.value for m in navigation.get("caption")]
    assert "Capacity: 1 | Confirmed bookings: 1" in [m.value for m in photography.get("caption")]
    assert any("Remaining places: 0" in m.value for m in photography.get("markdown"))
    for workshop_id, status in (
        ("workshop-1", "BOOKING OPEN"),
        ("workshop-2", "FULL / WAITLIST OPEN"),
        ("workshop-3", "BOOKING CLOSED"),
        ("workshop-4", "STARTED"),
    ):
        card = rendered_workshop(app, workshop_id)
        assert any(m.value.endswith(f"[{status}]") for m in card.get("markdown"))
        assert f"Workshop ID {workshop_id}" in [m.value for m in card.get("caption")]
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


@pytest.mark.parametrize("capacity", [1, 30])
def test_l4_booking_allocates_one_complete_independent_candidate(
    workshop: Workshop, capacity: int
) -> None:
    state = create_demo_state()
    state.workshops.append(replace(workshop, capacity=capacity))
    state.next_workshop_id = 2
    before = deepcopy(state)
    actor = resolve_actor(state, "participant-1")
    outcome, candidate = booking.book_workshop(state, actor, "workshop-1", now=NOW)
    assert outcome == "OK"
    expected = Registration(
        "registration-1",
        "workshop-1",
        "participant-1",
        RegistrationStatus.CONFIRMED,
        NOW.astimezone(UTC),
        NOW.astimezone(UTC),
    )
    assert candidate == replace(before, registrations=[expected], next_registration_id=2)
    assert state == before and candidate is not state
    for name in ("users", "workshops", "registrations"):
        assert getattr(candidate, name) is not getattr(state, name)


@pytest.mark.parametrize(
    ("actor", "expected"),
    [
        (None, "INVALID_ACTOR"),
        (DemoUser("unknown", "Xingjian", Role.PARTICIPANT), "INVALID_ACTOR"),
        (DemoUser("organiser-1", "Rui Yan", Role.PARTICIPANT), "INVALID_ACTOR"),
        (DemoUser("participant-1", "Xingjian", Role.ORGANISER), "INVALID_ACTOR"),
        (DemoUser("organiser-1", "Rui Yan", Role.ORGANISER), "FORBIDDEN"),
        (DemoUser("organiser-2", "Alex", Role.ORGANISER), "FORBIDDEN"),
    ],
)
def test_l4_booking_role_denials_preserve_all_data(
    populated_state: DemoState, actor: DemoUser | None, expected: str
) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.book_workshop(populated_state, actor, "workshop-1", now=NOW)
    assert outcome == expected
    assert result is populated_state and result == before


def test_l4_unknown_booking_target_is_explicit_without_mutation(populated_state: DemoState) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.book_workshop(
        populated_state, resolve_actor(populated_state, "participant-2"), "workshop-999", now=NOW
    )
    assert outcome == "UNKNOWN_WORKSHOP"
    assert result is populated_state and result == before


@pytest.mark.parametrize("offset", [-1, 0, 1, 86400, 86401])
def test_l4_booking_uses_strict_cutoff_even_with_spare_capacity(
    populated_state: DemoState, offset: int
) -> None:
    state = populated_state
    now = state.workshops[0].registration_cutoff + timedelta(seconds=offset)
    before = deepcopy(state)
    outcome, result = booking.book_workshop(
        state, resolve_actor(state, "participant-2"), "workshop-1", now=now
    )
    assert outcome == ("OK" if offset < 0 else "REGISTRATION_CLOSED")
    assert state == before
    if offset < 0:
        assert len(result.registrations) == len(before.registrations) + 1
        assert result.registrations[-1].created_at == now.astimezone(UTC)
        assert result.next_registration_id == before.next_registration_id + 1
    else:
        assert result is state and result == before


@pytest.mark.parametrize("now", [None, datetime(2026, 12, 1, 9)])
def test_l4_booking_rejects_an_unusable_clock_without_allocating(
    populated_state: DemoState, now: object
) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.book_workshop(
        populated_state, resolve_actor(populated_state, "participant-2"), "workshop-1", now=now
    )
    assert outcome == "INVALID_INPUT"
    assert result is populated_state and result == before


@pytest.mark.parametrize("zone", [UTC, ZoneInfo("America/New_York")])
def test_l4_booking_compares_actual_instants_across_zones(
    populated_state: DemoState, zone: object
) -> None:
    state = populated_state
    cutoff = state.workshops[0].registration_cutoff
    for seconds, expected in [(-1, "OK"), (0, "REGISTRATION_CLOSED")]:
        outcome, _ = booking.book_workshop(
            state,
            resolve_actor(state, "participant-2"),
            "workshop-1",
            now=(cutoff + timedelta(seconds=seconds)).astimezone(zone),
        )
        assert outcome == expected


def test_l4_full_booking_does_not_waitlist_or_advance_ids(populated_state: DemoState) -> None:
    state = populated_state
    state.workshops[0] = replace(state.workshops[0], capacity=1)
    before = deepcopy(state)
    outcome, result = booking.book_workshop(
        state, resolve_actor(state, "participant-2"), "workshop-1", now=NOW
    )
    assert outcome == "FULL"
    assert result is state and result == before
    assert {r.status for r in result.registrations} == {
        RegistrationStatus.CONFIRMED,
        RegistrationStatus.CANCELLED,
    }


def test_l4_duplicate_with_spare_capacity_keeps_original_id(populated_state: DemoState) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.book_workshop(
        populated_state, resolve_actor(populated_state, "participant-1"), "workshop-1", now=NOW
    )
    assert outcome == "DUPLICATE_ACTIVE"
    assert result is populated_state and result == before


@pytest.mark.parametrize("closed", [False, True])
def test_l4_booking_rejection_precedence_is_time_then_duplicate_then_full(
    populated_state: DemoState, closed: bool
) -> None:
    state = populated_state
    state.workshops[0] = replace(state.workshops[0], capacity=1)
    before = deepcopy(state)
    outcome, result = booking.book_workshop(
        state,
        resolve_actor(state, "participant-1"),
        "workshop-1",
        now=state.workshops[0].registration_cutoff if closed else NOW,
    )
    assert outcome == ("REGISTRATION_CLOSED" if closed else "DUPLICATE_ACTIVE")
    assert result is state and result == before


def test_l4_serial_last_place_and_repeated_request_use_the_latest_state(workshop: Workshop) -> None:
    original = create_demo_state()
    original.workshops.append(replace(workshop, capacity=1))
    original.next_workshop_id = 2
    before = deepcopy(original)
    outcome, latest = booking.book_workshop(
        original, resolve_actor(original, "participant-1"), "workshop-1", now=NOW
    )
    assert outcome == "OK"
    accepted = deepcopy(latest)
    for actor_id, expected in [("participant-2", "FULL"), ("participant-1", "DUPLICATE_ACTIVE")]:
        outcome, result = booking.book_workshop(
            latest, resolve_actor(latest, actor_id), "workshop-1", now=NOW
        )
        assert outcome == expected
        assert result is latest and result == accepted
    assert confirmed_count(latest, "workshop-1") == 1
    assert latest.next_registration_id == 2 and original == before


def test_l4_rebooking_retains_cancelled_history_and_allows_an_overlapping_workshop(
    populated_state: DemoState,
) -> None:
    state = populated_state
    state.workshops.append(replace(state.workshops[0], workshop_id="workshop-2"))
    state.next_workshop_id = 3
    before = deepcopy(state)
    outcome, first = booking.book_workshop(
        state, resolve_actor(state, "participant-2"), "workshop-1", now=NOW
    )
    assert outcome == "OK"
    outcome, second = booking.book_workshop(
        first, resolve_actor(first, "participant-2"), "workshop-2", now=NOW
    )
    assert outcome == "OK"
    assert second.registrations[:2] == before.registrations
    assert second.registrations[1].status == RegistrationStatus.CANCELLED
    assert [r.registration_id for r in second.registrations] == [
        "registration-1",
        "registration-2",
        "registration-3",
        "registration-4",
    ]
    assert second.next_registration_id == 5 and state == before


def test_l4_registration_construction_failure_preserves_complete_input(
    populated_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = deepcopy(populated_state)

    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("injected construction failure")

    monkeypatch.setattr(booking, "Registration", fail)
    with pytest.raises(RuntimeError, match="injected construction failure"):
        booking.book_workshop(
            populated_state, resolve_actor(populated_state, "participant-2"), "workshop-1", now=NOW
        )
    assert populated_state == before


@pytest.mark.parametrize("actor_id", ["participant-1", "participant-2"])
def test_l4_own_records_filter_by_id_and_keep_all_statuses(
    demo_data: DemoState, actor_id: str
) -> None:
    state = demo_data
    state.users[1] = replace(state.users[1], display_name=state.users[0].display_name)
    before = deepcopy(state)
    outcome, rows = booking.list_own_registrations(state, resolve_actor(state, actor_id))
    assert outcome == "OK"
    assert rows == tuple(r for r in before.registrations if r.participant_id == actor_id)
    assert rows and all(r.participant_id == actor_id for r in rows)
    assert state == before


@pytest.mark.parametrize("actor_id", [None, "unknown", "organiser-1", "organiser-2"])
def test_l4_private_read_denials_return_no_records(
    demo_data: DemoState, actor_id: str | None
) -> None:
    before = deepcopy(demo_data)
    outcome, rows = booking.list_own_registrations(demo_data, resolve_actor(demo_data, actor_id))
    assert outcome == (
        "FORBIDDEN" if actor_id and actor_id.startswith("organiser") else "INVALID_ACTOR"
    )
    assert rows == () and demo_data == before


def test_l4_empty_personal_history_is_a_successful_empty_read() -> None:
    state = create_demo_state()
    outcome, rows = booking.list_own_registrations(state, resolve_actor(state, "participant-1"))
    assert outcome == "OK" and rows == ()


def test_l4_ui_booking_updates_counts_own_history_and_owned_roster(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    original = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    preserved_forms = {
        "organiser-2": {
            "draft": {
                "new_title": "Retained fictional draft",
                "new_start_date": (NOW + timedelta(days=2)).date(),
                "new_start_time": time(9),
                "new_end_date": (NOW + timedelta(days=2)).date(),
                "new_end_time": time(11),
                "new_location": "",
                "new_capacity": 1,
                "new_notes": "Fictional preparation notes.",
            },
            "errors": {"location": "Meeting point is required."},
            "feedback": CREATION_REJECTED,
        }
    }
    app.session_state.creation_forms = deepcopy(preserved_forms)
    app.button(key="book_workshop-1").click().run()
    assert not app.exception and not app.error
    assert "registration-5" in app.success[0].value
    accepted = deepcopy(app.session_state.demo_state)
    assert len(accepted.registrations) == 5 and accepted.next_registration_id == 6
    assert accepted.registrations[:4] == original.registrations
    assert accepted.workshops == original.workshops and accepted.next_workshop_id == 5
    assert app.session_state.selected_user_id == "participant-2"
    assert app.session_state.creation_forms == preserved_forms
    assert app.metric[1].value == "4"
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    frames = [table.value for table in app.dataframe]
    assert len(frames) == 2
    assert set(frames[0]["Registration ID"]) == {"registration-2", "registration-5"}
    assert set(frames[1]["Registration ID"]) == {"registration-4"}
    assert set(frames[0]["Status"]) == {"CONFIRMED"}
    assert set(frames[1]["Status"]) == {"CANCELLED"}
    app.sidebar.button(key="refresh_view").click().run()
    assert app.session_state.demo_state == accepted
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    assert len(app.dataframe) == 1
    assert set(app.dataframe[0].value["Registration ID"]) == {"registration-1", "registration-3"}
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-1").run()
    assert set(app.dataframe[0].value["Participant"]) == {"Xingjian", "Sam"}
    assert app.session_state.demo_state == accepted and demo_data == original


@pytest.mark.parametrize(
    ("target", "expected"), [("workshop-1", "DUPLICATE_ACTIVE"), ("workshop-2", "FULL")]
)
def test_l4_ui_rejection_keeps_every_record_and_counter(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, target: str, expected: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.button(key=f"book_{target}").click().run()
    assert not app.exception and not app.success
    assert any(expected in e.value for e in app.error)
    assert app.session_state.demo_state is demo_data and demo_data == before


def test_l4_stale_booking_ui_uses_fresh_time_at_the_operation(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    rendered = app.button(key="book_workshop-1")
    assert not rendered.disabled
    monkeypatch.setattr(booking, "server_now", lambda: demo_data.workshops[0].registration_cutoff)
    rendered.click().run()
    assert not app.exception and not app.success
    assert any("REGISTRATION_CLOSED" in e.value for e in app.error)
    assert app.session_state.demo_state is demo_data and demo_data == before


@pytest.mark.parametrize("actor_id", [None, "organiser-1", "organiser-2"])
def test_l4_booking_controls_are_participant_only(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, actor_id: str | None
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value(actor_id).run()
    assert not [button for button in app.button if str(button.key).startswith("book_")]
    assert not app.exception


def test_l4_locked_and_started_booking_controls_are_disabled(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    assert app.button(key="book_workshop-3").disabled
    assert app.button(key="book_workshop-4").disabled
    assert not app.button(key="book_workshop-1").disabled
    assert not app.button(key="book_workshop-2").disabled


def test_l4_started_confirmed_record_is_history_without_status_change(
    populated_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = populated_state
    monkeypatch.setattr(booking, "server_now", lambda: state.workshops[0].ends_at)
    before = deepcopy(state)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert "Booking History" in [h.value for h in app.subheader]
    assert len(app.dataframe) == 1
    assert list(app.dataframe[0].value["Status"]) == ["CONFIRMED"]
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-1"]
    assert state == before and not app.exception


@pytest.mark.parametrize("outcome", ["FORBIDDEN", "UNEXPECTED"])
def test_l4_personal_ui_does_not_render_records_on_non_ok_result(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    monkeypatch.setattr(
        booking, "list_own_registrations", lambda *args: (outcome, tuple(demo_data.registrations))
    )
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert not app.exception and app.error
    assert not app.dataframe and demo_data == before


def test_l4_booking_isolated_from_another_session_and_failure_ui_preserves_input(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    other = create_demo_data(NOW)
    other_before = deepcopy(other)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.button(key="book_workshop-1").click().run()
    assert not app.exception and app.success
    assert other == other_before and len(app.session_state.demo_state.registrations) == 5
    current = app.session_state.demo_state
    before = deepcopy(current)

    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("injected booking failure")

    monkeypatch.setattr(booking, "book_workshop", fail)
    app.button(key="book_workshop-1").click().run()
    assert app.exception and "injected booking failure" in app.exception[0].message
    assert not app.success and app.session_state.demo_state is current and current == before


@pytest.mark.parametrize("path", ["success-reset", "draft-restore"])
def test_l4_creation_restoration_and_reset_do_not_log_duplicate_defaults(
    demo_data: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    path: str,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.session_state.review_marker = {"keep": ["fictional review data"]}
    before = deepcopy(demo_data)
    fill_creation_form(app, NOW + timedelta(hours=48))
    if path == "draft-restore":
        app.text_input(key="new_location").set_value("")
        app.number_input(key="new_capacity").set_value(31)
        app.button(key="create_workshop").click().run()
        failed_values = creation_form_values(app)
        app.sidebar.radio(key="current_view").set_value("Workshops").run()

    # Streamlit logs this warning once per process. Re-enable it as on a fresh server.
    monkeypatch.setattr("streamlit.elements.lib.policies._shown_default_value_warning", False)
    caplog.set_level("WARNING", logger="streamlit.elements.lib.policies")
    caplog.clear()
    if path == "success-reset":
        app.button(key="create_workshop").click().run()
        candidate = app.session_state.demo_state
        assert app.success and not app.error
        assert len(candidate.workshops) == len(before.workshops) + 1
        assert candidate.next_workshop_id == before.next_workshop_id + 1
        assert candidate.registrations == before.registrations
        assert candidate.next_registration_id == before.next_registration_id
        assert creation_form_values(app)["start_date"] == (NOW + timedelta(days=3)).date()
        assert creation_form_values(app)["capacity"] == 10
    else:
        app.sidebar.radio(key="current_view").set_value("Organiser").run()
        assert app.session_state.demo_state is demo_data
        assert creation_form_values(app) == failed_values
        assert {row.value for row in app.error} == {
            CREATION_REJECTED,
            "Meeting point is required.",
            "Capacity must be a whole number from 1 to 30.",
        }
    assert not app.exception
    assert demo_data == before
    assert app.session_state.selected_user_id == "organiser-1"
    assert app.session_state.review_marker == {"keep": ["fictional review data"]}
    assert not [
        record for record in caplog.records if "created with a default value" in record.getMessage()
    ]


@pytest.mark.parametrize("seconds", [-1, 0, 1])
def test_l4_personal_history_moves_at_start_without_rewriting_records(
    populated_state: DemoState, monkeypatch: pytest.MonkeyPatch, seconds: int
) -> None:
    state = populated_state
    now = state.workshops[0].starts_at + timedelta(seconds=seconds)
    monkeypatch.setattr(booking, "server_now", lambda: now)
    before = deepcopy(state)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert not app.exception and len(app.dataframe) == 1
    nodes = list(app.main)
    current_index = next(
        i
        for i, n in enumerate(nodes)
        if n.type == "subheader" and n.value == "Upcoming Confirmed Bookings"
    )
    history_index = next(
        i for i, n in enumerate(nodes) if n.type == "subheader" and n.value == "Booking History"
    )
    table_index = next(i for i, n in enumerate(nodes) if n is app.dataframe[0])
    if seconds < 0:
        assert current_index < table_index < history_index
    else:
        assert history_index < table_index
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-1"]
    assert list(app.dataframe[0].value["Status"]) == ["CONFIRMED"]
    assert app.session_state.demo_state is state and state == before


@pytest.mark.parametrize("outcome", ["FORBIDDEN", "UNEXPECTED"])
def test_l4_booking_ui_never_adopts_a_rejected_candidate(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    rejected = replace(demo_data, registrations=[], next_registration_id=999)
    monkeypatch.setattr(booking, "book_workshop", lambda *args, **kwargs: (outcome, rejected))
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.button(key="book_workshop-1").click().run()
    assert not app.exception and not app.success
    assert any(outcome in item.value for item in app.error)
    assert app.session_state.demo_state is demo_data and demo_data == before


@pytest.mark.parametrize("route", ["public", "other-organiser"])
@pytest.mark.parametrize(
    ("widget", "key", "invalid", "message"),
    [
        ("number_input", "new_capacity", 0, "Capacity must be a whole number from 1 to 30."),
        ("date_input", "new_start_date", None, "Choose a valid start date and time."),
        ("date_input", "new_end_date", None, "Choose a valid end date and time."),
        ("time_input", "new_start_time", None, "Choose a valid start date and time."),
        ("time_input", "new_end_time", None, "Choose a valid end date and time."),
    ],
)
def test_l4_f08_review_restores_invalid_values_without_substitution(
    demo_data: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    route: str,
    widget: str,
    key: str,
    invalid: object,
    message: str,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    getattr(app, widget)(key=key).set_value(invalid)
    app.button(key="create_workshop").click().run()
    rejected_values = creation_form_values(app)
    assert {e.value for e in app.error} == {CREATION_REJECTED, message}
    assert app.session_state.creation_forms["organiser-1"]["draft"][key] == invalid
    if route == "public":
        app.sidebar.radio(key="current_view").set_value("Workshops").run()
        app.sidebar.radio(key="current_view").set_value("Organiser").run()
    else:
        app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
        assert not app.error
        fill_creation_form(app, NOW + timedelta(hours=72))
        app.text_input(key="new_title").set_value("Alex's separate failure")
        app.text_input(key="new_location").set_value("")
        app.button(key="create_workshop").click().run()
        other_before = deepcopy(app.session_state.creation_forms["organiser-2"])
        app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
        assert app.session_state.creation_forms["organiser-2"] == other_before
    assert not app.exception and not app.success
    assert creation_form_values(app) == rejected_values
    assert {e.value for e in app.error} == {CREATION_REJECTED, message}
    assert app.session_state.selected_user_id == "organiser-1"
    assert app.session_state.demo_state is demo_data and demo_data == before


@pytest.mark.parametrize("outcome", ["INVALID_INPUT", "FORBIDDEN"])
def test_l4_f08_review_creation_refusal_does_not_adopt_a_different_candidate(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=72))
    app.text_input(key="new_title").set_value("")
    app.button(key="create_workshop").click().run()
    other_before = deepcopy(app.session_state.creation_forms["organiser-2"])
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    submitted_values = creation_form_values(app)
    refused = replace(
        demo_data, workshops=[], registrations=[], next_workshop_id=900, next_registration_id=901
    )
    monkeypatch.setattr(booking, "create_workshop", lambda *args, **kwargs: (outcome, refused))
    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.success
    assert [e.value for e in app.error] == [
        CREATION_REJECTED
        if outcome == "INVALID_INPUT"
        else "FORBIDDEN: Only organisers may create workshops."
    ]
    assert app.session_state.demo_state is demo_data and demo_data == before
    assert creation_form_values(app) == submitted_values
    assert app.session_state.creation_forms["organiser-2"] == other_before
    assert len(app.session_state.creation_forms["organiser-1"]["draft"]) == 8


@pytest.mark.parametrize("owner_id", ["participant-1", "participant-2"])
@pytest.mark.parametrize("capacity", [1, 30])
def test_l5_cancel_retains_one_history_row_and_returns_an_independent_complete_state(
    populated_state: DemoState, owner_id: str, capacity: int
) -> None:
    state = populated_state
    state.workshops[0] = replace(state.workshops[0], capacity=capacity)
    state.registrations[0] = replace(state.registrations[0], participant_id=owner_id)
    before = deepcopy(state)
    outcome, candidate = booking.cancel_registration(
        state, resolve_actor(state, owner_id), "registration-1", now=NOW
    )
    expected_row = replace(
        before.registrations[0], status=RegistrationStatus.CANCELLED, updated_at=NOW.astimezone(UTC)
    )
    assert outcome == "OK"
    assert candidate == replace(before, registrations=[expected_row, before.registrations[1]])
    assert candidate is not state and state == before
    assert confirmed_count(candidate, "workshop-1") == confirmed_count(before, "workshop-1") - 1
    assert candidate.workshops[0].capacity - confirmed_count(candidate, "workshop-1") == capacity
    for name in ("users", "workshops", "registrations"):
        assert getattr(candidate, name) is not getattr(state, name)


@pytest.mark.parametrize(
    ("actor", "expected"),
    [
        (None, "INVALID_ACTOR"),
        (DemoUser("unknown", "Xingjian", Role.PARTICIPANT), "INVALID_ACTOR"),
        (DemoUser("organiser-1", "Rui Yan", Role.PARTICIPANT), "INVALID_ACTOR"),
        (DemoUser("participant-1", "Xingjian", Role.ORGANISER), "INVALID_ACTOR"),
        (DemoUser("organiser-1", "Rui Yan", Role.ORGANISER), "FORBIDDEN"),
        (DemoUser("organiser-2", "Alex", Role.ORGANISER), "FORBIDDEN"),
    ],
)
def test_l5_cancel_role_denials_preserve_every_record_and_counter(
    populated_state: DemoState, actor: DemoUser | None, expected: str
) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.cancel_registration(populated_state, actor, "registration-1", now=NOW)
    assert outcome == expected
    assert result is populated_state and result == before


@pytest.mark.parametrize(
    ("actor_id", "target"),
    [("participant-2", "registration-1"), ("participant-1", "registration-2")],
)
def test_l5_cancel_checks_the_stored_owner_even_for_cancelled_targets(
    populated_state: DemoState, actor_id: str, target: str
) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.cancel_registration(
        populated_state, resolve_actor(populated_state, actor_id), target, now=NOW
    )
    assert outcome == "FORBIDDEN"
    assert result is populated_state and result == before


def test_l5_equal_display_names_do_not_grant_cancellation_ownership(
    populated_state: DemoState,
) -> None:
    state = populated_state
    state.users[1] = replace(state.users[1], display_name="Xingjian")
    before = deepcopy(state)
    outcome, result = booking.cancel_registration(
        state, resolve_actor(state, "participant-2"), "registration-1", now=NOW
    )
    assert outcome == "FORBIDDEN" and result is state and state == before


def test_l5_unknown_registration_is_explicit_and_does_not_change_state(
    populated_state: DemoState,
) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.cancel_registration(
        populated_state,
        resolve_actor(populated_state, "participant-1"),
        "registration-999",
        now=NOW,
    )
    assert outcome == "UNKNOWN_REGISTRATION"
    assert result is populated_state and result == before


@pytest.mark.parametrize("offset", [-1, 0, 1, 86400, 86401])
def test_l5_effective_cancellation_requires_strictly_before_cutoff(
    populated_state: DemoState, offset: int
) -> None:
    state = populated_state
    now = state.workshops[0].registration_cutoff + timedelta(seconds=offset)
    before = deepcopy(state)
    outcome, result = booking.cancel_registration(
        state, resolve_actor(state, "participant-1"), "registration-1", now=now
    )
    assert outcome == ("OK" if offset < 0 else "REGISTRATION_CLOSED")
    assert state == before
    if offset < 0:
        assert result.registrations[0] == replace(
            before.registrations[0], status=RegistrationStatus.CANCELLED, updated_at=now
        )
        assert confirmed_count(result, "workshop-1") == 0
        assert result.next_registration_id == before.next_registration_id
    else:
        assert result is state and result == before


@pytest.mark.parametrize("zone", [UTC, ZoneInfo("America/New_York")])
def test_l5_cancellation_compares_equivalent_aware_instants(
    populated_state: DemoState, zone: object
) -> None:
    state = populated_state
    before = deepcopy(state)
    for offset, expected in [(-1, "OK"), (0, "REGISTRATION_CLOSED")]:
        now = (state.workshops[0].registration_cutoff + timedelta(seconds=offset)).astimezone(zone)
        outcome, result = booking.cancel_registration(
            state, resolve_actor(state, "participant-1"), "registration-1", now=now
        )
        assert outcome == expected and state == before
        if expected == "OK":
            assert result.registrations[0].updated_at == now.astimezone(UTC)
        else:
            assert result is state


@pytest.mark.parametrize("now", [None, datetime(2026, 12, 1, 9)])
def test_l5_active_cancellation_rejects_an_unusable_application_clock(
    populated_state: DemoState, now: object
) -> None:
    before = deepcopy(populated_state)
    outcome, result = booking.cancel_registration(
        populated_state, resolve_actor(populated_state, "participant-1"), "registration-1", now=now
    )
    assert outcome == "INVALID_INPUT" and result is populated_state and result == before


@pytest.mark.parametrize("offset", [-1, 0, 1, 86400, 86401])
def test_l5_owned_cancelled_repeat_is_a_no_op_before_and_after_cutoff_and_start(
    populated_state: DemoState, offset: int
) -> None:
    state = populated_state
    before = deepcopy(state)
    now = state.workshops[0].registration_cutoff + timedelta(seconds=offset)
    outcome, result = booking.cancel_registration(
        state, resolve_actor(state, "participant-2"), "registration-2", now=now
    )
    assert outcome == "ALREADY_CANCELLED" and result is state and state == before
    assert confirmed_count(result, "workshop-1") == 1


def test_l5_missing_referenced_workshop_does_not_release_a_place(
    populated_state: DemoState,
) -> None:
    state = populated_state
    state.workshops.clear()  # Internal inconsistent fixture, not a workshop-deletion feature.
    before = deepcopy(state)
    outcome, result = booking.cancel_registration(
        state, resolve_actor(state, "participant-1"), "registration-1", now=NOW
    )
    assert outcome == "UNKNOWN_WORKSHOP" and result is state and state == before


def test_l5_cancel_construction_exception_preserves_complete_input(
    populated_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = deepcopy(populated_state)
    original_replace = booking.replace

    def fail_on_registration(value: object, **changes: object):
        if isinstance(value, Registration):
            raise RuntimeError("injected cancellation construction failure")
        return original_replace(value, **changes)

    monkeypatch.setattr(booking, "replace", fail_on_registration)
    with pytest.raises(RuntimeError, match="injected cancellation construction failure"):
        booking.cancel_registration(
            populated_state,
            resolve_actor(populated_state, "participant-1"),
            "registration-1",
            now=NOW,
        )
    assert populated_state == before


@pytest.mark.parametrize("next_actor_id", ["participant-1", "participant-2"])
def test_l5_serial_cancel_rebook_and_repeat_preserve_history_and_one_place(
    populated_state: DemoState, next_actor_id: str
) -> None:
    state = populated_state
    state.workshops[0] = replace(state.workshops[0], capacity=1)
    before = deepcopy(state)
    outcome, full = booking.book_workshop(
        state, resolve_actor(state, "participant-2"), "workshop-1", now=NOW
    )
    assert outcome == "FULL" and full is state
    outcome, cancelled = booking.cancel_registration(
        state, resolve_actor(state, "participant-1"), "registration-1", now=NOW
    )
    assert outcome == "OK" and confirmed_count(cancelled, "workshop-1") == 0
    outcome, rebooked = booking.book_workshop(
        cancelled,
        resolve_actor(cancelled, next_actor_id),
        "workshop-1",
        now=NOW + timedelta(seconds=1),
    )
    assert outcome == "OK" and rebooked.registrations[-1].registration_id == "registration-3"
    assert rebooked.registrations[-1].participant_id == next_actor_id
    assert rebooked.registrations[:2] == cancelled.registrations
    snapshot = deepcopy(rebooked)
    for instant in [
        NOW + timedelta(seconds=2),
        state.workshops[0].registration_cutoff,
        state.workshops[0].ends_at,
    ]:
        outcome, repeated = booking.cancel_registration(
            rebooked, resolve_actor(rebooked, "participant-1"), "registration-1", now=instant
        )
        assert outcome == "ALREADY_CANCELLED" and repeated is rebooked and rebooked == snapshot
        assert confirmed_count(repeated, "workshop-1") == 1
    other_id = "participant-2" if next_actor_id == "participant-1" else "participant-1"
    outcome, refused = booking.book_workshop(
        rebooked, resolve_actor(rebooked, other_id), "workshop-1", now=NOW + timedelta(seconds=3)
    )
    assert outcome == "FULL" and refused is rebooked
    assert rebooked.next_registration_id == 4 and state == before


def test_l5_ui_cancel_updates_history_capacity_and_owned_roster_without_losing_drafts(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    saved_forms = {
        "organiser-1": {
            "draft": {"new_title": "Fictional Rui draft"},
            "errors": {"location": "Meeting point is required."},
            "feedback": CREATION_REJECTED,
        }
    }
    app.session_state.creation_forms = deepcopy(saved_forms)
    app.session_state.review_marker = {"keep": ["fictional L5 review"]}
    app.button(key="cancel_registration-2").click().run()
    assert not app.exception and not app.error
    assert any("registration-2" in item.value for item in app.success)
    candidate = app.session_state.demo_state
    expected_rows = before.registrations.copy()
    expected_rows[1] = replace(
        expected_rows[1], status=RegistrationStatus.CANCELLED, updated_at=NOW.astimezone(UTC)
    )
    assert candidate == replace(before, registrations=expected_rows)
    assert app.session_state.selected_user_id == "participant-2"
    assert app.session_state.current_view == "My Bookings"
    assert app.session_state.creation_forms == saved_forms
    assert app.session_state.review_marker == {"keep": ["fictional L5 review"]}
    assert app.metric[1].value == "2" and len(app.dataframe) == 1
    assert set(app.dataframe[0].value["Registration ID"]) == {"registration-2", "registration-4"}
    assert set(app.dataframe[0].value["Status"]) == {"CANCELLED"}
    assert not [b for b in app.button if str(b.key).startswith("cancel_")]
    app.sidebar.button(key="refresh_view").click().run()
    assert app.session_state.demo_state == candidate and not app.success
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    assert not app.success
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    card = rendered_workshop(app, "workshop-2")
    assert "Capacity: 1 | Confirmed bookings: 0" in [m.value for m in card.get("caption")]
    assert any("Remaining places: 1" in m.value for m in card.get("markdown"))
    app.button(key="book_workshop-2").click().run()
    assert app.session_state.demo_state.registrations[-1].registration_id == "registration-5"
    assert app.session_state.demo_state.next_registration_id == 6
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-2").run()
    assert list(app.dataframe[0].value["Participant"]) == ["Xingjian"]
    assert app.session_state.creation_forms["organiser-1"] == saved_forms["organiser-1"]
    assert demo_data == before


@pytest.mark.parametrize(
    ("actor_id", "expected"),
    [
        ("participant-1", {"cancel_registration-1", "cancel_registration-3"}),
        ("participant-2", {"cancel_registration-2"}),
    ],
)
def test_l5_ui_exposes_only_own_confirmed_cancellation_targets(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, actor_id: str, expected: set[str]
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value(actor_id).run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert {b.key for b in app.button if str(b.key).startswith("cancel_")} == expected
    if actor_id == "participant-1":
        assert app.button(key="cancel_registration-3").disabled
        assert not app.button(key="cancel_registration-1").disabled
    assert not app.exception


@pytest.mark.parametrize("actor_id", [None, "organiser-1", "organiser-2"])
def test_l5_non_participants_have_no_cancellation_menu_or_controls(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, actor_id: str | None
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value(actor_id).run()
    assert "My Bookings" not in app.sidebar.radio(key="current_view").options
    assert not [b for b in app.button if str(b.key).startswith("cancel_")]
    assert not app.exception and app.session_state.demo_state is demo_data and demo_data == before


@pytest.mark.parametrize("offset", [0, 86400, 86401])
def test_l5_ui_disables_effective_cancellation_at_cutoff_and_after_start(
    populated_state: DemoState, monkeypatch: pytest.MonkeyPatch, offset: int
) -> None:
    now = populated_state.workshops[0].registration_cutoff + timedelta(seconds=offset)
    monkeypatch.setattr(booking, "server_now", lambda: now)
    before = deepcopy(populated_state)
    app = app_with_state(populated_state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    if offset == 0:
        assert app.button(key="cancel_registration-1").disabled
    else:
        assert not any(button.key == "cancel_registration-1" for button in app.button)
        assert list(app.dataframe[0].value["Status"]) == ["CONFIRMED"]
        assert list(app.dataframe[0].value["Registration ID"]) == ["registration-1"]
    assert not app.exception and app.session_state.demo_state is populated_state
    assert populated_state == before


@pytest.mark.parametrize("offset", [0, 1])
def test_l5_stale_cancellation_ui_uses_fresh_decision_time(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, offset: int
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    rendered = app.button(key="cancel_registration-2")
    assert not rendered.disabled
    decision = demo_data.workshops[1].registration_cutoff + timedelta(seconds=offset)
    monkeypatch.setattr(booking, "server_now", lambda: decision)
    rendered.click().run()
    assert not app.exception and not app.success
    assert any("REGISTRATION_CLOSED" in e.value for e in app.error)
    assert app.session_state.demo_state is demo_data and demo_data == before


@pytest.mark.parametrize("outcome", ["FORBIDDEN", "ALREADY_CANCELLED", "UNEXPECTED"])
def test_l5_ui_never_adopts_a_non_ok_cancellation_candidate(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    refused = replace(demo_data, registrations=[], next_workshop_id=900, next_registration_id=901)
    monkeypatch.setattr(booking, "cancel_registration", lambda *args, **kwargs: (outcome, refused))
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    app.button(key="cancel_registration-2").click().run()
    assert not app.exception and not app.success
    assert any(outcome in e.value for e in [*app.error, *app.info])
    assert app.session_state.demo_state is demo_data and demo_data == before


def test_l5_ui_cancellation_exception_keeps_the_original_business_snapshot(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)

    def fail(*args: object, **kwargs: object):
        raise RuntimeError("injected cancellation call failure")

    monkeypatch.setattr(booking, "cancel_registration", fail)
    before = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    app.button(key="cancel_registration-2").click().run()
    assert app.exception and not app.success
    assert app.session_state.demo_state is demo_data and demo_data == before


def test_l5_cancel_in_one_session_does_not_change_an_independent_session(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    first, second = create_demo_data(NOW), create_demo_data(NOW)
    second_before = deepcopy(second)
    app = app_with_state(first)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    app.button(key="cancel_registration-2").click().run()
    assert (
        not app.exception
        and app.session_state.demo_state.registrations[1].status == RegistrationStatus.CANCELLED
    )
    other = app_with_state(second)
    other.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    other.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert not other.exception and not other.button(key="cancel_registration-2").disabled
    assert other.session_state.demo_state is second and second == second_before


@pytest.mark.parametrize(
    ("target_id", "owner_id"),
    [("registration-1", "participant-1"), ("registration-3", "participant-2")],
)
@pytest.mark.parametrize("reverse", [False, True])
def test_l5_review_cancel_changes_only_target_among_multiple_confirmations(
    populated_state: DemoState, target_id: str, owner_id: str, reverse: bool
) -> None:
    state = populated_state
    state.workshops[0] = replace(state.workshops[0], capacity=2)
    state.workshops.append(
        replace(state.workshops[0], workshop_id="workshop-2", owner_id="organiser-2")
    )
    created = NOW - timedelta(hours=1)
    state.registrations.extend(
        [
            Registration(
                "registration-3",
                "workshop-1",
                "participant-2",
                RegistrationStatus.CONFIRMED,
                created,
                created,
            ),
            Registration(
                "registration-4",
                "workshop-2",
                "participant-1",
                RegistrationStatus.CONFIRMED,
                created,
                created,
            ),
        ]
    )
    state.next_workshop_id, state.next_registration_id = 3, 5
    if reverse:
        state.registrations.reverse()
    before = deepcopy(state)
    assert confirmed_count(state, "workshop-1") == 2
    assert confirmed_count(state, "workshop-2") == 1
    outcome, candidate = booking.cancel_registration(
        state, resolve_actor(state, owner_id), target_id, now=NOW
    )
    expected_rows = before.registrations.copy()
    index = next(i for i, row in enumerate(expected_rows) if row.registration_id == target_id)
    expected_rows[index] = replace(
        expected_rows[index], status=RegistrationStatus.CANCELLED, updated_at=NOW.astimezone(UTC)
    )
    assert outcome == "OK" and candidate == replace(before, registrations=expected_rows)
    assert confirmed_count(candidate, "workshop-1") == 1
    assert confirmed_count(candidate, "workshop-2") == 1
    assert [r.registration_id for r in candidate.registrations] == [
        r.registration_id for r in before.registrations
    ]
    assert candidate.next_workshop_id == 3 and candidate.next_registration_id == 5
    assert state == before and candidate is not state


@pytest.mark.parametrize("route", ["domain", "ui"])
def test_l5_review_final_state_construction_failure_preserves_domain_and_ui_input(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, route: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    before = deepcopy(demo_data)
    original_rows = demo_data.registrations
    if route == "ui":
        app = app_with_state(demo_data)
        app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
        app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    original_replace = booking.replace

    def fail_on_final_state(value: object, **changes: object):
        if isinstance(value, DemoState):
            raise RuntimeError("injected final candidate construction failure")
        return original_replace(value, **changes)

    monkeypatch.setattr(booking, "replace", fail_on_final_state)
    if route == "domain":
        with pytest.raises(RuntimeError, match="injected final candidate construction failure"):
            booking.cancel_registration(
                demo_data, resolve_actor(demo_data, "participant-2"), "registration-2", now=NOW
            )
    else:
        app.button(key="cancel_registration-2").click().run()
        assert app.exception and not app.success
        assert "injected final candidate construction failure" in app.exception[0].value
        assert app.session_state.demo_state is demo_data
        assert app.session_state.selected_user_id == "participant-2"
    assert demo_data == before and demo_data.registrations is original_rows
    assert confirmed_count(demo_data, "workshop-2") == 1


@pytest.mark.parametrize("target_id", ["registration-2", "registration-5"])
def test_l5_review_ui_cancels_the_clicked_booking_when_two_are_eligible(
    demo_data: DemoState, monkeypatch: pytest.MonkeyPatch, target_id: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    original = deepcopy(demo_data)
    app = app_with_state(demo_data)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.button(key="book_workshop-1").click().run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert {b.key for b in app.button if str(b.key).startswith("cancel_")} == {
        "cancel_registration-2",
        "cancel_registration-5",
    }
    assert not app.button(key="cancel_registration-2").disabled
    assert not app.button(key="cancel_registration-5").disabled
    previous = app.session_state.demo_state
    before = deepcopy(previous)
    now = NOW + timedelta(seconds=5)
    monkeypatch.setattr(booking, "server_now", lambda: now)
    app.button(key=f"cancel_{target_id}").click().run()
    expected_rows = before.registrations.copy()
    index = next(i for i, row in enumerate(expected_rows) if row.registration_id == target_id)
    expected_rows[index] = replace(
        expected_rows[index], status=RegistrationStatus.CANCELLED, updated_at=now.astimezone(UTC)
    )
    assert not app.exception and not app.error
    assert any(target_id in item.value for item in app.success)
    candidate = app.session_state.demo_state
    assert candidate == replace(before, registrations=expected_rows)
    assert candidate.next_workshop_id == 5 and candidate.next_registration_id == 6
    other_id = "registration-5" if target_id == "registration-2" else "registration-2"
    assert set(app.dataframe[0].value["Registration ID"]) == {other_id}
    assert set(app.dataframe[1].value["Registration ID"]) == {"registration-4", target_id}
    assert set(app.dataframe[1].value["Status"]) == {"CANCELLED"}
    assert previous == before and demo_data == original
    assert app.session_state.selected_user_id == "participant-2"


@pytest.mark.parametrize(
    ("organiser_id", "first_participant", "replacement_participant"),
    [
        ("organiser-1", "participant-1", "participant-2"),
        ("organiser-2", "participant-2", "participant-1"),
    ],
)
def test_l6_created_workshop_completes_the_v1_baseline_journey(
    monkeypatch: pytest.MonkeyPatch,
    organiser_id: str,
    first_participant: str,
    replacement_participant: str,
) -> None:
    """Integrate real UI entry points; existing tests cover multi-attendee targeting."""
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    initial = create_demo_state()
    before = deepcopy(initial)
    app = app_with_state(initial)
    assert app.sidebar.radio(key="current_view").options == ["Workshops"]
    app.sidebar.selectbox(key="selected_user_id").set_value(organiser_id).run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    fill_creation_form(app, NOW + timedelta(hours=48))
    app.text_input(key="new_location").set_value(" ")
    failed_values = creation_form_values(app)
    app.button(key="create_workshop").click().run()
    assert [item.value for item in app.error] == [CREATION_REJECTED, "Meeting point is required."]
    assert creation_form_values(app) == failed_values
    assert app.session_state.demo_state is initial and initial == before
    assert (initial.next_workshop_id, initial.next_registration_id) == (1, 1)

    app.text_input(key="new_location").set_value("East Trail Entrance")
    app.button(key="create_workshop").click().run()
    assert not app.exception and not app.error
    created = app.session_state.demo_state
    assert len(created.workshops) == 1 and created.registrations == []
    workshop = created.workshops[0]
    assert (workshop.workshop_id, workshop.owner_id, workshop.capacity) == (
        "workshop-1",
        organiser_id,
        1,
    )
    assert workshop.starts_at == NOW + timedelta(hours=48)
    assert workshop.registration_cutoff == NOW + timedelta(hours=24)
    assert (created.next_workshop_id, created.next_registration_id) == (2, 1)
    assert app.text_input(key="new_title").value == ""
    assert app.number_input(key="new_capacity").value == 10
    assert not app.session_state.creation_forms[organiser_id].get("draft")
    assert initial == before

    app.sidebar.selectbox(key="selected_user_id").set_value(first_participant).run()
    assert app.sidebar.radio(key="current_view").value == "Workshops"
    assert app.sidebar.radio(key="current_view").options == ["Workshops", "My Bookings"]
    app.button(key="book_workshop-1").click().run()
    booked = app.session_state.demo_state
    first_row = Registration(
        "registration-1",
        "workshop-1",
        first_participant,
        RegistrationStatus.CONFIRMED,
        NOW.astimezone(UTC),
        NOW.astimezone(UTC),
    )
    assert booked == replace(created, registrations=[first_row], next_registration_id=2)
    assert created.registrations == [] and created.next_registration_id == 1
    # Explicit duplicate-before-capacity precedence: this fixture is also full.
    # Retained spare-capacity tests independently establish B09 duplicate refusal.
    app.button(key="book_workshop-1").click().run()
    assert any(item.value.startswith("DUPLICATE_ACTIVE:") for item in app.error)
    assert app.session_state.demo_state is booked

    app.sidebar.selectbox(key="selected_user_id").set_value(replacement_participant).run()
    app.button(key="book_workshop-1").click().run()
    assert any(item.value.startswith("FULL:") for item in app.error)
    assert app.session_state.demo_state is booked and booked.registrations == [first_row]
    assert booked.next_registration_id == 2
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert not app.dataframe
    assert not any(str(button.key).startswith("cancel_") for button in app.button)

    app.sidebar.selectbox(key="selected_user_id").set_value(first_participant).run()
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-1"]
    app.button(key="cancel_registration-1").click().run()
    cancelled = app.session_state.demo_state
    cancelled_row = replace(first_row, status=RegistrationStatus.CANCELLED)
    assert cancelled == replace(booked, registrations=[cancelled_row])
    assert booked.registrations == [first_row] and confirmed_count(cancelled, "workshop-1") == 0
    assert list(app.dataframe[0].value["Status"]) == ["CANCELLED"]

    app.sidebar.selectbox(key="selected_user_id").set_value(replacement_participant).run()
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    app.button(key="book_workshop-1").click().run()
    final = app.session_state.demo_state
    replacement_row = replace(
        first_row, registration_id="registration-2", participant_id=replacement_participant
    )
    assert final == replace(
        cancelled, registrations=[cancelled_row, replacement_row], next_registration_id=3
    )
    assert cancelled.registrations == [cancelled_row] and cancelled.next_registration_id == 2
    assert confirmed_count(final, "workshop-1") == 1

    app.sidebar.selectbox(key="selected_user_id").set_value(organiser_id).run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-2"]
    assert list(app.dataframe[0].value["Participant ID"]) == [replacement_participant]
    other_organiser = "organiser-2" if organiser_id == "organiser-1" else "organiser-1"
    app.sidebar.selectbox(key="selected_user_id").set_value(other_organiser).run()
    assert not app.dataframe and app.session_state.demo_state is final

    monkeypatch.setattr(booking, "server_now", lambda: NOW + timedelta(hours=24))
    app.sidebar.selectbox(key="selected_user_id").set_value(replacement_participant).run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert app.button(key="cancel_registration-2").disabled
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    assert app.button(key="book_workshop-1").disabled
    app.sidebar.selectbox(key="selected_user_id").set_value(None).run()
    assert app.sidebar.radio(key="current_view").options == ["Workshops"]
    assert app.session_state.demo_state is final and not app.exception


@pytest.mark.parametrize("operation", ["create", "book"])
@pytest.mark.parametrize("route", ["domain", "ui"])
def test_l6_review_final_candidate_failure_preserves_creation_and_booking_input(
    monkeypatch: pytest.MonkeyPatch, operation: str, route: str
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    state = create_demo_data(NOW)
    before = deepcopy(state)
    original_lists = (state.users, state.workshops, state.registrations)
    actor_id = "organiser-1" if operation == "create" else "participant-2"
    if route == "ui":
        app = app_with_state(state)
        app.sidebar.selectbox(key="selected_user_id").set_value(actor_id).run()
        if operation == "create":
            app.sidebar.radio(key="current_view").set_value("Organiser").run()
            fill_creation_form(app, NOW + timedelta(hours=48))
            submitted = creation_form_values(app)
    original_replace = booking.replace

    def fail_final_candidate(value: object, **changes: object):
        if isinstance(value, DemoState):
            raise RuntimeError("injected final create/book candidate failure")
        return original_replace(value, **changes)

    monkeypatch.setattr(booking, "replace", fail_final_candidate)
    if route == "domain":
        with pytest.raises(RuntimeError, match="injected final create/book candidate failure"):
            if operation == "create":
                create_workshop(
                    state,
                    resolve_actor(state, actor_id),
                    title="Fictional candidate failure check",
                    starts_at=NOW + timedelta(hours=48),
                    ends_at=NOW + timedelta(hours=50),
                    location="East Trail Entrance",
                    capacity=1,
                    now=NOW,
                )
            else:
                booking.book_workshop(state, resolve_actor(state, actor_id), "workshop-1", now=NOW)
    else:
        key = "create_workshop" if operation == "create" else "book_workshop-1"
        app.button(key=key).click().run()
        assert app.exception and not app.success
        assert "injected final create/book candidate failure" in app.exception[0].value
        assert app.session_state.demo_state is state
        assert app.session_state.selected_user_id == actor_id
        if operation == "create":
            assert creation_form_values(app) == submitted
    assert state == before
    assert state.users is original_lists[0]
    assert state.workshops is original_lists[1]
    assert state.registrations is original_lists[2]
    assert (state.next_workshop_id, state.next_registration_id) == (5, 5)


@pytest.mark.parametrize("git_mode", ["absent", "detached", "branch", "invalid"])
def test_l6_runtime_identity_is_read_only_and_explicit_about_git_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, git_mode: str
) -> None:
    from hashlib import sha256

    import app as application

    fixtures = {
        "app.py": b"fixture application\n",
        "booking.py": b"fixture business module\n",
        "requirements.txt": b"streamlit==1.67.0\npyarrow==24.0.0\n",
    }
    for name, raw in fixtures.items():
        (tmp_path / name).write_bytes(raw)
    expected_sha = None
    if git_mode != "absent":
        (tmp_path / ".git").mkdir()
        head = tmp_path / ".git/HEAD"
        if git_mode == "detached":
            head.write_text("1" * 40 + "\n")
            expected_sha = "1" * 40
        elif git_mode == "branch":
            head.write_text("ref: refs/heads/codex/review\n")
            ref = tmp_path / ".git/refs/heads/codex/review"
            ref.parent.mkdir(parents=True)
            ref.write_text("2" * 40 + "\n")
            expected_sha = "2" * 40
        else:
            head.write_text("unverified-text\n")
    expected_packages = {"streamlit": "1.67.0", "pyarrow": "24.0.0"}
    monkeypatch.setattr(application, "version", lambda name: expected_packages[name])
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    result = application.runtime_identity(tmp_path)
    assert result == {
        "git_sha": expected_sha,
        "python": application.platform.python_version(),
        "source_sha256": {name: sha256(raw).hexdigest() for name, raw in fixtures.items()},
        "runtime_packages": expected_packages,
    }
    assert {
        p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()
    } == before


def test_l6_runtime_identity_logs_once_without_changing_business_state(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    import json

    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    state = create_demo_state()
    before = deepcopy(state)
    app = app_with_state(state)
    messages = [
        line
        for line in capsys.readouterr().out.splitlines()
        if line.startswith("L6_RUNTIME_IDENTITY ")
    ]
    assert len(messages) == 1
    identity = json.loads(messages[0].removeprefix("L6_RUNTIME_IDENTITY "))
    assert set(identity) == {"git_sha", "python", "source_sha256", "runtime_packages"}
    assert set(identity["source_sha256"]) == {"app.py", "booking.py", "requirements.txt"}
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    assert not any(
        line.startswith("L6_RUNTIME_IDENTITY ") for line in capsys.readouterr().out.splitlines()
    )
    assert not app.exception and app.session_state.demo_state is state and state == before


@pytest.fixture
def l8_state(workshop: Workshop) -> DemoState:
    state = create_demo_state()
    state.users.extend(
        [
            DemoUser("fixture-fifo-alpha", "FIFO Test Alpha", Role.PARTICIPANT),
            DemoUser("fixture-fifo-zulu", "FIFO Test Zulu", Role.PARTICIPANT),
        ]
    )
    state.workshops = [
        replace(workshop, capacity=1),
        replace(workshop, workshop_id="workshop-2", owner_id="organiser-2", capacity=1),
    ]
    state.registrations = [
        Registration(
            "registration-1", "workshop-1", "participant-1", RegistrationStatus.CONFIRMED, NOW, NOW
        ),
        Registration(
            "registration-2", "workshop-2", "participant-1", RegistrationStatus.CONFIRMED, NOW, NOW
        ),
    ]
    state.next_workshop_id = 3
    state.next_registration_id = 3
    return state


def l8_participant(state: DemoState, user_id: str) -> DemoUser:
    actor = resolve_actor(state, user_id)
    assert actor is not None and actor.user_id == user_id and actor.role is Role.PARTICIPANT
    return actor


def test_l8_explicit_join_keeps_full_book_and_confirmed_counts(l8_state: DemoState) -> None:
    state = l8_state
    before = deepcopy(state)
    alpha = l8_participant(state, "fixture-fifo-alpha")
    assert booking.book_workshop(state, alpha, "workshop-1", now=NOW) == ("FULL", state)
    outcome, joined = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    stamp = NOW.astimezone(UTC)
    record = Registration(
        "registration-3",
        "workshop-1",
        alpha.user_id,
        RegistrationStatus.WAITLISTED,
        stamp,
        stamp,
        1,
    )
    assert outcome == "OK" and joined == replace(
        before, registrations=[*before.registrations, record], next_registration_id=4
    )
    assert (
        state == before
        and joined.users is not state.users
        and joined.workshops is not state.workshops
    )
    assert confirmed_count(joined, "workshop-1") == 1
    assert booking.book_workshop(joined, alpha, "workshop-1", now=NOW) == (
        "DUPLICATE_ACTIVE",
        joined,
    )
    assert booking.join_waitlist(joined, alpha, "workshop-1", now=NOW) == (
        "DUPLICATE_ACTIVE",
        joined,
    )
    assert booking.join_waitlist(
        state, l8_participant(state, "participant-1"), "workshop-1", now=NOW
    ) == ("DUPLICATE_ACTIVE", state)
    zulu = l8_participant(joined, "fixture-fifo-zulu")
    assert booking.book_workshop(joined, zulu, "workshop-1", now=NOW) == ("FULL", joined)
    assert joined.registrations == [*before.registrations, record]


def test_l8_spare_seat_requires_book_and_inconsistent_queue_prevents_bypass(
    l8_state: DemoState,
) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    state.registrations.pop(0)
    before = deepcopy(state)
    outcome, returned = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "USE_BOOKING" and returned is state and state == before
    state.registrations.append(
        Registration(
            "registration-3",
            "workshop-1",
            "fixture-fifo-zulu",
            RegistrationStatus.WAITLISTED,
            NOW,
            NOW,
            1,
        )
    )
    state.next_registration_id = 4
    before = deepcopy(state)
    outcome, returned = booking.book_workshop(state, alpha, "workshop-1", now=NOW)
    assert outcome == "INTEGRITY_ERROR" and returned is state and state == before


@pytest.mark.parametrize("reverse_time", [False, True], ids=["equal-times", "later-sequence-older"])
def test_l8_fifo_ignores_list_names_timestamps_and_other_queues(
    l8_state: DemoState, reverse_time: bool
) -> None:
    state = l8_state
    confirmed = replace(state.registrations[0], registration_id="registration-10")
    early = Registration(
        "registration-13",
        "workshop-1",
        "fixture-fifo-zulu",
        RegistrationStatus.WAITLISTED,
        NOW,
        NOW,
        3,
    )
    alpha_time = NOW - timedelta(seconds=1) if reverse_time else NOW
    later = Registration(
        "registration-18",
        "workshop-1",
        "fixture-fifo-alpha",
        RegistrationStatus.WAITLISTED,
        alpha_time,
        alpha_time,
        8,
    )
    withdrawn = Registration(
        "registration-11", "workshop-1", "participant-2", RegistrationStatus.CANCELLED, NOW, NOW, 1
    )
    foreign = replace(
        withdrawn,
        registration_id="registration-21",
        workshop_id="workshop-2",
        status=RegistrationStatus.WAITLISTED,
    )
    state.registrations = [later, confirmed, withdrawn, foreign, early, state.registrations[1]]
    state.next_registration_id = 30
    before = deepcopy(state)
    decision = datetime(2026, 12, 9, 8, 59, 59, tzinfo=WORKSHOP_TIMEZONE)
    stamp = decision.astimezone(UTC)
    owner = l8_participant(state, "participant-1")
    alpha = l8_participant(state, "fixture-fifo-alpha")
    zulu = l8_participant(state, "fixture-fifo-zulu")
    assert booking.list_own_waitlist_positions(state, zulu) == ("OK", {"registration-13": 1})
    assert booking.list_own_waitlist_positions(state, alpha) == ("OK", {"registration-18": 2})
    assert booking.get_workshop_waitlist(
        state, resolve_actor(state, "organiser-1"), "workshop-1"
    ) == ("OK", (early, later))
    outcome, result = booking.cancel_registration(state, owner, "registration-10", now=decision)
    expected = [
        later,
        replace(confirmed, status=RegistrationStatus.CANCELLED, updated_at=stamp),
        withdrawn,
        foreign,
        replace(early, status=RegistrationStatus.CONFIRMED, updated_at=stamp),
        before.registrations[-1],
    ]
    assert outcome == "OK" and result == replace(before, registrations=expected)
    assert state == before and result.registrations is not state.registrations
    assert confirmed_count(result, "workshop-1") == confirmed_count(result, "workshop-2") == 1
    assert booking.list_own_waitlist_positions(result, alpha) == ("OK", {"registration-18": 1})
    assert booking.list_own_waitlist_positions(result, zulu) == ("OK", {})
    assert booking.cancel_registration(
        result, owner, "registration-10", now=decision + timedelta(seconds=1)
    ) == ("ALREADY_CANCELLED", result)


@pytest.mark.parametrize("another_waiter", [False, True], ids=["empty-queue", "active-head"])
def test_l8_withdraw_and_rejoin_after_highest_sequence_preserves_history(
    l8_state: DemoState, another_waiter: bool
) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    zulu = l8_participant(state, "fixture-fifo-zulu")
    if another_waiter:
        outcome, state = booking.join_waitlist(state, zulu, "workshop-1", now=NOW)
        assert outcome == "OK"
    outcome, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    target = state.registrations[-1]
    before = deepcopy(state)
    withdraw_at = NOW + timedelta(minutes=1)
    outcome, withdrawn = booking.withdraw_waitlist(
        state, alpha, target.registration_id, now=withdraw_at
    )
    assert outcome == "OK" and state == before
    expected = replace(
        target, status=RegistrationStatus.CANCELLED, updated_at=withdraw_at.astimezone(UTC)
    )
    assert withdrawn == replace(before, registrations=[*before.registrations[:-1], expected])
    outcome, result = booking.join_waitlist(withdrawn, alpha, "workshop-1", now=withdraw_at)
    assert outcome == "OK"
    rejoined = result.registrations[-1]
    assert (rejoined.registration_id, rejoined.queue_seq) == (
        ("registration-5", 3) if another_waiter else ("registration-4", 2)
    )
    assert result.registrations[:-1] == withdrawn.registrations
    assert result.next_registration_id == withdrawn.next_registration_id + 1
    next_outcome, other = booking.join_waitlist(result, zulu, "workshop-2", now=withdraw_at)
    assert next_outcome == "OK" and other.registrations[-1].queue_seq == 1
    assert other.registrations[:-1] == result.registrations


@pytest.mark.parametrize("join_first", [True, False], ids=["join-then-cancel", "cancel-then-join"])
def test_l8_serial_actions_use_the_previous_result(l8_state: DemoState, join_first: bool) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    owner = l8_participant(state, "participant-1")
    if join_first:
        outcome, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
        assert outcome == "OK"
    outcome, cancelled = booking.cancel_registration(state, owner, "registration-1", now=NOW)
    assert outcome == "OK" and cancelled.registrations[0].status is RegistrationStatus.CANCELLED
    if join_first:
        assert cancelled.registrations[-1].registration_id == "registration-3"
        assert cancelled.registrations[-1].status is RegistrationStatus.CONFIRMED
        assert cancelled.registrations[-1].queue_seq == 1
        assert cancelled.next_registration_id == state.next_registration_id
    else:
        assert confirmed_count(cancelled, "workshop-1") == 0
        assert booking.join_waitlist(cancelled, alpha, "workshop-1", now=NOW) == (
            "USE_BOOKING",
            cancelled,
        )
        outcome, booked = booking.book_workshop(cancelled, alpha, "workshop-1", now=NOW)
        assert outcome == "OK" and booked.registrations[-1].status is RegistrationStatus.CONFIRMED
        assert booked.registrations[-1].queue_seq is None


@pytest.mark.parametrize(
    ("offset", "allocation", "withdrawal"),
    [
        (-1, "OK", "OK"),
        (0, "REGISTRATION_CLOSED", "OK"),
        (1, "REGISTRATION_CLOSED", "OK"),
        (86399, "REGISTRATION_CLOSED", "OK"),
        (86400, "REGISTRATION_CLOSED", "WORKSHOP_STARTED"),
        (86401, "REGISTRATION_CLOSED", "WORKSHOP_STARTED"),
    ],
)
def test_l8_cutoff_and_start_distinguish_effective_operations(
    l8_state: DemoState, offset: int, allocation: str, withdrawal: str
) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    zulu = l8_participant(state, "fixture-fifo-zulu")
    owner = l8_participant(state, "participant-1")
    outcome, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    before = deepcopy(state)
    cutoff = datetime(2026, 12, 9, 9, tzinfo=WORKSHOP_TIMEZONE)
    decision = cutoff + timedelta(seconds=offset)
    outcome, joined = booking.join_waitlist(state, zulu, "workshop-1", now=decision)
    assert outcome == allocation
    if allocation == "OK":
        assert joined.registrations[-1].queue_seq == 2 and joined.next_registration_id == 5
    else:
        assert joined is state
    outcome, cancelled = booking.cancel_registration(state, owner, "registration-1", now=decision)
    assert outcome == allocation
    if allocation == "OK":
        assert [row.status for row in cancelled.registrations] == [
            RegistrationStatus.CANCELLED,
            RegistrationStatus.CONFIRMED,
            RegistrationStatus.CONFIRMED,
        ]
        assert cancelled.next_registration_id == 4
    else:
        assert cancelled is state
    outcome, withdrawn = booking.withdraw_waitlist(state, alpha, "registration-3", now=decision)
    assert outcome == withdrawal
    if withdrawal == "OK":
        assert withdrawn == replace(
            before,
            registrations=[
                *before.registrations[:2],
                replace(
                    before.registrations[2],
                    status=RegistrationStatus.CANCELLED,
                    updated_at=decision.astimezone(UTC),
                ),
            ],
        )
        assert booking.withdraw_waitlist(
            withdrawn, alpha, "registration-3", now=cutoff + timedelta(days=1)
        ) == ("ALREADY_CANCELLED", withdrawn)
    else:
        assert withdrawn is state
    assert state == before


@pytest.mark.parametrize("offset", [-1, 0, 1, 86400])
def test_l8_d01_preserves_confirmed_booking_after_stale_withdrawal(
    l8_state: DemoState, offset: int
) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    owner = l8_participant(state, "participant-1")
    outcome, joined = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    outcome, promoted = booking.cancel_registration(joined, owner, "registration-1", now=NOW)
    assert outcome == "OK" and promoted.registrations[-1].status is RegistrationStatus.CONFIRMED
    before = deepcopy(promoted)
    decision = datetime(2026, 12, 9, 9, tzinfo=WORKSHOP_TIMEZONE) + timedelta(seconds=offset)
    outcome, same = booking.withdraw_waitlist(promoted, alpha, "registration-3", now=decision)
    assert outcome == "STATUS_CHANGED" and same is promoted and same == before


def test_l8_d01_checks_identity_owner_target_and_noop_before_status_or_clock(
    l8_state: DemoState,
) -> None:
    state = l8_state
    owner = l8_participant(state, "participant-1")
    alpha = l8_participant(state, "fixture-fifo-alpha")
    organizer = resolve_actor(state, "organiser-1")
    invalid_clock = NOW.replace(tzinfo=None)
    before = deepcopy(state)
    cases = [
        (organizer, "registration-1", "FORBIDDEN"),
        (alpha, "registration-1", "FORBIDDEN"),
        (None, "registration-1", "INVALID_ACTOR"),
        (owner, "missing", "UNKNOWN_REGISTRATION"),
        (owner, "registration-1", "STATUS_CHANGED"),
    ]
    for actor, registration_id, expected in cases:
        outcome, result = booking.withdraw_waitlist(
            state, actor, registration_id, now=invalid_clock
        )
        assert outcome == expected and result is state and state == before
    missing_workshop = replace(state, workshops=state.workshops[1:])
    assert booking.withdraw_waitlist(
        missing_workshop, owner, "registration-1", now=invalid_clock
    ) == ("UNKNOWN_WORKSHOP", missing_workshop)
    outcome, joined = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    assert booking.cancel_registration(joined, alpha, "registration-3", now=invalid_clock) == (
        "STATUS_CHANGED",
        joined,
    )
    assert booking.withdraw_waitlist(joined, alpha, "registration-3", now=invalid_clock) == (
        "INVALID_INPUT",
        joined,
    )
    outcome, withdrawn = booking.withdraw_waitlist(joined, alpha, "registration-3", now=NOW)
    assert outcome == "OK"
    for action in (booking.withdraw_waitlist, booking.cancel_registration):
        outcome, same = action(withdrawn, alpha, "registration-3", now=invalid_clock)
        assert outcome == "ALREADY_CANCELLED" and same is withdrawn
        assert action(withdrawn, owner, "registration-3", now=invalid_clock) == (
            "FORBIDDEN",
            withdrawn,
        )


@pytest.mark.parametrize(
    "bad_actor",
    ["unknown", "organiser-1", "fixture-fifo-alpha"],
    ids=["unknown", "organiser-1", "participant-leo"],
)
def test_l8_waitlist_reads_and_mutations_respect_actor_and_workshop_scope(
    l8_state: DemoState, bad_actor: str
) -> None:
    state = l8_state
    zulu = l8_participant(state, "fixture-fifo-zulu")
    outcome, state = booking.join_waitlist(state, zulu, "workshop-2", now=NOW)
    assert outcome == "OK"
    before = deepcopy(state)
    actor = resolve_actor(state, bad_actor)
    expected = "INVALID_ACTOR" if actor is None else "FORBIDDEN"
    assert booking.get_workshop_waitlist(state, actor, "workshop-2") == (expected, ())
    assert booking.withdraw_waitlist(state, actor, "registration-3", now=NOW) == (expected, state)
    assert booking.get_workshop_waitlist(
        state, resolve_actor(state, "organiser-2"), "workshop-2"
    ) == ("OK", (state.registrations[-1],))
    assert state == before


def test_l8_promotion_fault_does_not_adopt_half_cancellation(
    l8_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    outcome, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    before = deepcopy(state)
    original_replace = booking.replace
    attempted_statuses = []

    def fail_on_promotion(value: object, **changes: object):
        if isinstance(value, Registration):
            attempted_statuses.append(changes["status"])
            if value.status is RegistrationStatus.WAITLISTED:
                raise RuntimeError("injected promotion construction failure")
        return original_replace(value, **changes)

    monkeypatch.setattr(booking, "replace", fail_on_promotion)
    with pytest.raises(RuntimeError, match="injected promotion construction failure"):
        booking.cancel_registration(
            state, l8_participant(state, "participant-1"), "registration-1", now=NOW
        )
    assert attempted_statuses == [RegistrationStatus.CANCELLED, RegistrationStatus.CONFIRMED]
    assert state == before and confirmed_count(state, "workshop-1") == 1


def test_l8_ui_join_promote_refresh_and_read_owned_queue(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(create_demo_data(NOW))
    identity = app.sidebar.selectbox(key="selected_user_id")
    identity.set_value("participant-1").run()
    assert {"Leo (PARTICIPANT)", "Willy (PARTICIPANT)"} <= set(identity.options)
    assert not any("FIFO Test" in option for option in identity.options)
    app.button(key="book_workshop-2").click().run()
    assert any("FULL:" in error.value for error in app.error)
    assert len(app.session_state.demo_state.registrations) == 4
    app.button(key="join_workshop-2").click().run()
    assert any("WAITLISTED" in message.value for message in app.success)
    assert confirmed_count(app.session_state.demo_state, "workshop-2") == 1
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert any(
        "Position" in frame.value and list(frame.value["Position"]) == [1]
        for frame in app.dataframe
    )
    assert app.button(key="withdraw_registration-5")
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-2").run()
    assert list(app.dataframe[0].value["Participant"]) == ["Sam"]
    assert list(app.dataframe[1].value["Participant"]) == ["Xingjian"]
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    assert all(
        "registration-5" not in list(frame.value["Registration ID"]) for frame in app.dataframe
    )
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert not any(str(button.key).startswith("withdraw_") for button in app.button)
    app.button(key="cancel_registration-2").click().run()
    assert any("One waiting participant was promoted" in message.value for message in app.success)
    assert list(app.dataframe[0].value["Status"]) == ["CANCELLED", "CANCELLED"]
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.button(key="refresh_view").click().run()
    assert not app.exception
    assert "registration-5" in list(app.dataframe[0].value["Registration ID"])
    assert set(app.dataframe[0].value["Status"]) == {"CONFIRMED"}
    assert app.session_state.demo_state.next_registration_id == 6


def test_l8_ui_stale_withdrawal_uses_latest_state_and_original_intent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    state = create_demo_data(NOW)
    outcome, state = booking.join_waitlist(
        state, l8_participant(state, "participant-1"), "workshop-2", now=NOW
    )
    assert outcome == "OK"
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    stale = app.button(key="withdraw_registration-5")
    outcome, promoted = booking.cancel_registration(
        state, l8_participant(state, "participant-2"), "registration-2", now=NOW
    )
    assert outcome == "OK"
    before = deepcopy(promoted)
    app.session_state.demo_state = promoted
    stale.click().run()
    assert not app.exception and app.session_state.demo_state is promoted and promoted == before
    assert any("STATUS_CHANGED: Refresh" in error.value for error in app.error)
    assert not any(str(button.key).startswith("withdraw_") for button in app.button)


@pytest.mark.parametrize(
    "at_start", [False, True], ids=["withdraw-at-cutoff", "stale-withdraw-at-start"]
)
def test_l8_ui_uses_fresh_withdrawal_deadline(
    monkeypatch: pytest.MonkeyPatch, at_start: bool
) -> None:
    state = create_demo_data(NOW)
    outcome, joined = booking.join_waitlist(
        state, l8_participant(state, "participant-1"), "workshop-2", now=NOW
    )
    assert outcome == "OK"
    workshop = state.workshops[1]
    monkeypatch.setattr(booking, "server_now", lambda: workshop.registration_cutoff)
    app = app_with_state(joined)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    assert app.button(key="join_workshop-2").disabled
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert not app.button(key="withdraw_registration-5").disabled
    before = deepcopy(joined)
    if at_start:
        monkeypatch.setattr(booking, "server_now", lambda: workshop.starts_at)
    app.button(key="withdraw_registration-5").click().run()
    assert not app.exception and confirmed_count(app.session_state.demo_state, "workshop-2") == 1
    row = app.session_state.demo_state.registrations[-1]
    if at_start:
        assert (
            row.status is RegistrationStatus.WAITLISTED and app.session_state.demo_state is joined
        )
        assert any("WORKSHOP_STARTED" in error.value for error in app.error)
        assert any(
            "Closed at workshop start" in list(frame.value.get("Waitlist", []))
            for frame in app.dataframe
        )
    else:
        assert row.status is RegistrationStatus.CANCELLED and row.queue_seq == 1
        assert any("Find the record in Booking History" in message.value for message in app.success)
    assert joined == before and app.session_state.demo_state.next_registration_id == 6


def test_l8_withdrawn_head_stays_cancelled_and_promoted_history_retains_sequence(
    l8_state: DemoState,
) -> None:
    state = l8_state
    alpha = l8_participant(state, "fixture-fifo-alpha")
    zulu = l8_participant(state, "fixture-fifo-zulu")
    owner = l8_participant(state, "participant-1")
    outcome, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    outcome, state = booking.join_waitlist(state, zulu, "workshop-1", now=NOW)
    assert outcome == "OK"
    outcome, state = booking.withdraw_waitlist(state, alpha, "registration-3", now=NOW)
    assert outcome == "OK" and state.registrations[0].registration_id == "registration-1"
    assert state.registrations[0].status is RegistrationStatus.CONFIRMED
    assert booking.list_own_waitlist_positions(state, zulu) == ("OK", {"registration-4": 1})
    outcome, state = booking.cancel_registration(state, owner, "registration-1", now=NOW)
    assert outcome == "OK"
    assert state.registrations[2].status is RegistrationStatus.CANCELLED
    assert state.registrations[3].status is RegistrationStatus.CONFIRMED
    assert state.registrations[3].queue_seq == 2
    outcome, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    assert (state.registrations[-1].registration_id, state.registrations[-1].queue_seq) == (
        "registration-5",
        3,
    )


def test_l8_ui_join_at_fresh_cutoff_preserves_open_view_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_demo_data(NOW)
    cutoff = state.workshops[1].registration_cutoff
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    before = deepcopy(state)
    rendered = app.button(key="join_workshop-2")
    assert not rendered.disabled
    monkeypatch.setattr(booking, "server_now", lambda: cutoff)
    rendered.click().run()
    assert not app.exception and not app.success
    assert any("REGISTRATION_CLOSED" in error.value for error in app.error)
    assert app.session_state.demo_state is state and state == before


def test_l8_ui_never_adopts_partial_promotion_on_fault(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    state = create_demo_data(NOW)
    outcome, state = booking.join_waitlist(
        state, l8_participant(state, "participant-1"), "workshop-2", now=NOW
    )
    assert outcome == "OK"
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    before = deepcopy(state)
    original_replace = booking.replace
    attempted = []

    def fail_after_cancellation(value: object, **changes: object):
        if isinstance(value, Registration):
            attempted.append(changes["status"])
            if value.status is RegistrationStatus.WAITLISTED:
                raise RuntimeError("injected UI promotion failure")
        return original_replace(value, **changes)

    monkeypatch.setattr(booking, "replace", fail_after_cancellation)
    app.button(key="cancel_registration-2").click().run()
    assert attempted == [RegistrationStatus.CANCELLED, RegistrationStatus.CONFIRMED]
    assert app.exception and not app.success
    assert app.session_state.demo_state is state and state == before


def test_l8_equal_display_names_keep_distinct_queue_entries(l8_state: DemoState) -> None:
    state = l8_state
    state.users = [
        replace(user, display_name="FIFO Test Alpha")
        if user.user_id == "fixture-fifo-zulu"
        else user
        for user in state.users
    ]
    alpha = l8_participant(state, "fixture-fifo-alpha")
    zulu = l8_participant(state, "fixture-fifo-zulu")
    assert alpha.display_name == zulu.display_name and alpha.user_id != zulu.user_id
    first, state = booking.join_waitlist(state, alpha, "workshop-1", now=NOW)
    second, state = booking.join_waitlist(state, zulu, "workshop-1", now=NOW)
    assert (first, second) == ("OK", "OK")
    assert booking.list_own_waitlist_positions(state, alpha) == ("OK", {"registration-3": 1})
    assert booking.list_own_waitlist_positions(state, zulu) == ("OK", {"registration-4": 2})
    assert [row.participant_id for row in state.registrations[-2:]] == [alpha.user_id, zulu.user_id]


def test_l8_review_stale_join_rechecks_capacity_and_keeps_the_seat_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    state = create_demo_data(NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    stale_join = app.button(key="join_workshop-2")
    outcome, reopened = booking.cancel_registration(
        state, l8_participant(state, "participant-2"), "registration-2", now=NOW
    )
    assert outcome == "OK" and confirmed_count(reopened, "workshop-2") == 0
    before = deepcopy(reopened)
    app.session_state.demo_state = reopened
    stale_join.click().run()
    assert not app.exception and not app.success
    assert any("USE_BOOKING" in error.value for error in app.error)
    assert app.session_state.demo_state is reopened and reopened == before
    assert not any(button.key == "join_workshop-2" for button in app.button)


def test_l8_review_stale_join_does_not_enrol_a_different_selected_participant(
    l8_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    state = l8_state
    before = deepcopy(state)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-alpha").run()
    stale_join = app.button(key="join_workshop-1")
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-zulu")
    stale_join.click().run()
    assert not app.exception and not app.success
    assert any("INVALID_ACTOR" in error.value for error in app.error)
    assert app.sidebar.selectbox(key="selected_user_id").value == "fixture-fifo-zulu"
    assert app.session_state.demo_state is state and state == before


def test_l8_review_closed_organiser_queue_keeps_history_without_live_position(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_demo_data(NOW)
    outcome, state = booking.join_waitlist(
        state, l8_participant(state, "participant-1"), "workshop-2", now=NOW
    )
    assert outcome == "OK"
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: state.workshops[1].starts_at)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-2").run()
    assert not app.exception and any(
        "Remaining entries are historical" in row.value for row in app.caption
    )
    waiting = app.dataframe[1].value
    assert "Position" not in waiting
    assert list(waiting["Queue order at close"]) == [1]
    assert list(waiting["Registration ID"]) == ["registration-5"]
    assert list(waiting["Status"]) == ["WAITLISTED"]
    assert app.session_state.demo_state is state and state == before


@pytest.mark.parametrize(
    ("seconds_from_cutoff", "available_label", "full_label", "disabled"),
    [
        (-1, "BOOKING OPEN", "FULL / WAITLIST OPEN", False),
        (0, "BOOKING CLOSED", "BOOKING CLOSED", True),
        (1, "BOOKING CLOSED", "BOOKING CLOSED", True),
        (86399, "BOOKING CLOSED", "BOOKING CLOSED", True),
        (86400, "STARTED", "STARTED", True),
        (86401, "STARTED", "STARTED", True),
    ],
    ids=["C-minus-1s", "C", "C-plus-1s", "S-minus-1s", "S", "S-plus-1s"],
)
def test_p1_workshop_status_is_scoped_to_card_and_display_time(
    l8_state: DemoState,
    monkeypatch: pytest.MonkeyPatch,
    seconds_from_cutoff: int,
    available_label: str,
    full_label: str,
    disabled: bool,
) -> None:
    full, open_with_space = l8_state.workshops
    state = replace(l8_state, workshops=[full, replace(open_with_space, capacity=2)])
    before = deepcopy(state)
    cutoff = datetime(2026, 12, 9, 9, tzinfo=WORKSHOP_TIMEZONE)
    monkeypatch.setattr(
        booking, "server_now", lambda: cutoff + timedelta(seconds=seconds_from_cutoff)
    )
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-alpha").run()
    for workshop_id, expected_label, places in (
        ("workshop-1", full_label, 0),
        ("workshop-2", available_label, 1),
    ):
        card = rendered_workshop(app, workshop_id)
        labels = [m.value for m in card.get("markdown") if "-badge[" in m.value]
        assert len(labels) == 1 and labels[0].endswith(f"[{expected_label}]")
        assert any(f"Remaining places: {places}" in m.value for m in card.get("markdown"))
        assert app.button(key=f"book_{workshop_id}").disabled is disabled
    assert app.button(key="join_workshop-1").disabled is disabled
    assert not any(button.key == "join_workshop-2" for button in app.button)
    assert not app.exception and app.session_state.demo_state is state and state == before


def test_p1_main_identity_and_role_update_with_sidebar_without_mutation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_demo_data(NOW)
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    states = (
        (None, "Fictional identity: None selected", ["Workshops"]),
        (
            "participant-1",
            "Fictional identity: Xingjian | Role: PARTICIPANT",
            ["Workshops", "My Bookings"],
        ),
        ("organiser-2", "Fictional identity: Alex | Role: ORGANISER", ["Workshops", "Organiser"]),
        (None, "Fictional identity: None selected", ["Workshops"]),
    )
    for identity, badge, menus in states:
        app.sidebar.selectbox(key="selected_user_id").set_value(identity).run()
        labels = [
            item.value for item in app.main.get("markdown") if "[Fictional identity:" in item.value
        ]
        assert len(labels) == 1 and labels[0].endswith(f"[{badge}]")
        assert not any("[Fictional identity:" in item.value for item in app.sidebar.markdown)
        assert app.sidebar.radio(key="current_view").options == menus
        assert any(
            "Demo identity selection is not secure authentication" in item.value
            for item in app.main.get("caption")
        )
        assert not app.exception and app.session_state.demo_state is state and state == before


def test_p1_groups_identified_controls_with_active_records_and_keeps_history_read_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_demo_data(NOW)
    actor = l8_participant(state, "participant-1")
    outcome, joined = booking.join_waitlist(state, actor, "workshop-2", now=NOW)
    assert outcome == "OK"
    outcome, withdrawn = booking.withdraw_waitlist(joined, actor, "registration-5", now=NOW)
    assert outcome == "OK"
    outcome, rejoined = booking.join_waitlist(withdrawn, actor, "workshop-2", now=NOW)
    assert outcome == "OK"
    before = deepcopy(rejoined)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(rejoined)
    app.sidebar.selectbox(key="selected_user_id").set_value(actor.user_id).run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    section_titles = ["Upcoming Confirmed Bookings", "My Waitlist", "Booking History"]
    assert [item.value for item in app.subheader] == ["My Bookings", *section_titles]
    nodes = list(app.main)
    start_at = [
        next(i for i, n in enumerate(nodes) if n.type == "subheader" and n.value == title)
        for title in section_titles
    ]
    confirmed, waiting, history = app.dataframe
    assert set(confirmed.value["Registration ID"]) == {"registration-1", "registration-3"}
    assert list(waiting.value["Registration ID"]) == ["registration-6"]
    assert list(waiting.value["Position"]) == [1]
    assert waiting.value.columns.get_loc("Position") < waiting.value.columns.get_loc("Start")
    assert list(history.value["Registration ID"]) == ["registration-5"]
    assert list(history.value["Status"]) == ["CANCELLED"]
    assert "Position" not in confirmed.value and "Position" not in history.value
    assert (
        start_at[0]
        < nodes.index(confirmed)
        < nodes.index(app.button(key="cancel_registration-1"))
        < start_at[1]
    )
    assert (
        start_at[1]
        < nodes.index(waiting)
        < nodes.index(app.button(key="withdraw_registration-6"))
        < start_at[2]
    )
    assert start_at[2] < nodes.index(history)
    assert not any(
        button.key in {"withdraw_registration-5", "cancel_registration-5"} for button in app.button
    )
    assert any(
        "including during the final 24 hours" in item.value
        and "There are no notifications." in item.value
        for item in nodes[start_at[1] : start_at[2]]
        if item.type == "caption"
    )
    assert not app.exception and app.session_state.demo_state is rejoined and rejoined == before


def test_p1_full_book_and_explicit_join_report_outcomes_and_next_actions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_demo_data(NOW)
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    card = rendered_workshop(app, "workshop-2")
    assert any(
        "WAITLISTED means unconfirmed" in item.value and "There are no notifications." in item.value
        for item in card.get("caption")
    )
    app.button(key="book_workshop-2").click().run()
    assert any(
        entry.value.startswith("FULL:") and "Join Waitlist" in entry.value for entry in app.error
    )
    assert not app.success and app.session_state.demo_state is state and state == before
    rendered_join = app.button(key="join_workshop-2")
    assert not rendered_join.disabled
    rendered_join.click().run()
    assert any(
        "WAITLISTED" in entry.value and "Open My Bookings" in entry.value for entry in app.success
    )
    joined = app.session_state.demo_state
    waiting = joined.registrations[-1]
    assert (waiting.registration_id, waiting.status, waiting.queue_seq) == (
        "registration-5",
        RegistrationStatus.WAITLISTED,
        1,
    )
    assert joined == replace(
        before, registrations=[*before.registrations, waiting], next_registration_id=6
    )
    joined_before = deepcopy(joined)
    assert app.button(key="join_workshop-2").disabled
    assert any(
        "You are already on this waitlist" in item.value
        for item in rendered_workshop(app, "workshop-2").get("caption")
    )

    stale_view = app_with_state(state)
    stale_view.sidebar.selectbox(key="selected_user_id").set_value("participant-1").run()
    stale_join = stale_view.button(key="join_workshop-2")
    assert not stale_join.disabled
    stale_view.session_state.demo_state = joined
    stale_join.click().run()
    assert any(
        entry.value.startswith("DUPLICATE_ACTIVE:") and "My Bookings" in entry.value
        for entry in rendered_workshop(stale_view, "workshop-2").get("error")
    )
    assert not stale_view.success and not stale_view.exception
    assert stale_view.session_state.demo_state is joined and joined == joined_before
    assert state == before


def test_p1_successful_book_and_cancel_with_no_waiter_report_the_released_place(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = create_demo_data(NOW)
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.button(key="book_workshop-1").click().run()
    assert any(
        "registration-5 (CONFIRMED)" in entry.value and "Open My Bookings" in entry.value
        for entry in app.success
    )
    booked = app.session_state.demo_state
    assert confirmed_count(booked, "workshop-1") == 2
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    app.button(key="cancel_registration-5").click().run()
    assert any(
        "One place released." in entry.value and "Booking History" in entry.value
        for entry in app.success
    )
    assert not any("promoted" in entry.value for entry in app.success)
    cancelled = replace(booked.registrations[-1], status=RegistrationStatus.CANCELLED)
    assert app.session_state.demo_state == replace(
        booked, registrations=[*before.registrations, cancelled]
    )
    assert confirmed_count(app.session_state.demo_state, "workshop-1") == 1
    assert not app.error and not app.exception and state == before


@pytest.mark.parametrize("transition", ["at-start", "already-cancelled"])
def test_p1_stale_cancel_preserves_intent_when_active_control_disappears(
    monkeypatch: pytest.MonkeyPatch, transition: str
) -> None:
    state = create_demo_data(NOW)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    stale = app.button(key="cancel_registration-2")
    assert not stale.disabled
    if transition == "at-start":
        monkeypatch.setattr(booking, "server_now", lambda: state.workshops[1].starts_at)
        current = state
        expected = "REGISTRATION_CLOSED"
    else:
        actor = l8_participant(state, "participant-2")
        outcome, current = booking.cancel_registration(state, actor, "registration-2", now=NOW)
        assert outcome == "OK"
        app.session_state.demo_state = current
        expected = "ALREADY_CANCELLED"
    before = deepcopy(current)
    stale.click().run()
    assert any(item.value.startswith(f"{expected}:") for item in [*app.error, *app.info])
    assert not any(button.key == "cancel_registration-2" for button in app.button)
    assert not app.exception and not app.success
    assert app.session_state.demo_state is current and current == before


@pytest.mark.parametrize(
    "next_identity", ["fixture-fifo-zulu", "organiser-2"], ids=["participant-willy", "organiser-2"]
)
def test_p1_review_stale_book_keeps_rendered_identity(
    l8_state: DemoState, monkeypatch: pytest.MonkeyPatch, next_identity: str
) -> None:
    workshop = replace(l8_state.workshops[0], capacity=2)
    state = replace(l8_state, workshops=[workshop, *l8_state.workshops[1:]])
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-alpha").run()
    stale_book = app.button(key="book_workshop-1")
    assert not stale_book.disabled
    app.sidebar.selectbox(key="selected_user_id").set_value(next_identity)
    stale_book.click().run()
    assert not app.exception and not app.success
    assert any(item.value.startswith("INVALID_ACTOR:") for item in app.error)
    assert app.sidebar.selectbox(key="selected_user_id").value == next_identity
    assert app.session_state.demo_state is state and state == before


def test_p1_acceptance_join_feedback_stays_on_other_full_workshop_card(
    l8_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    available = replace(l8_state.workshops[0], capacity=2)
    state = replace(l8_state, workshops=[available, *l8_state.workshops[1:]])
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-alpha").run()

    app.button(key="book_workshop-1").click().run()
    booked = app.session_state.demo_state
    assert booked.registrations[-1].status == RegistrationStatus.CONFIRMED
    app.button(key="book_workshop-2").click().run()
    assert any(
        error.value.startswith("FULL:")
        for error in rendered_workshop(app, "workshop-2").get("error")
    )
    assert app.session_state.demo_state is booked

    join = app.button(key="join_workshop-2")
    assert not join.disabled
    join.click().run()
    assert any(
        "WAITLISTED" in item.value and "Registration ID: registration-4" in item.value
        for item in rendered_workshop(app, "workshop-2").get("success")
    )
    assert not rendered_workshop(app, "workshop-1").get("success")
    joined = app.session_state.demo_state
    waiting = joined.registrations[-1]
    assert (waiting.participant_id, waiting.workshop_id, waiting.status) == (
        "fixture-fifo-alpha",
        "workshop-2",
        RegistrationStatus.WAITLISTED,
    )
    assert joined == replace(
        booked,
        registrations=[*booked.registrations, waiting],
        next_registration_id=booked.next_registration_id + 1,
    )
    assert app.button(key="join_workshop-2").disabled
    assert not app.exception and state == before


def test_p1_acceptance_last_seat_disables_same_workshop_join(
    l8_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    available = replace(l8_state.workshops[0], capacity=2)
    state = replace(l8_state, workshops=[available, *l8_state.workshops[1:]])
    before = deepcopy(state)
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-alpha").run()

    app.button(key="book_workshop-1").click().run()
    booked = app.session_state.demo_state
    row = booked.registrations[-1]
    assert (row.workshop_id, row.participant_id, row.status) == (
        "workshop-1",
        "fixture-fifo-alpha",
        RegistrationStatus.CONFIRMED,
    )
    assert booked == replace(
        before,
        registrations=[*before.registrations, row],
        next_registration_id=before.next_registration_id + 1,
    )
    assert confirmed_count(booked, "workshop-1") == available.capacity
    assert app.button(key="join_workshop-1").disabled
    assert any(
        "You already have a confirmed booking" in item.value
        for item in rendered_workshop(app, "workshop-1").get("caption")
    )
    assert not app.button(key="join_workshop-2").disabled
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-zulu").run()
    assert not app.button(key="join_workshop-1").disabled
    assert not app.exception and app.session_state.demo_state is booked and state == before


def test_p1_review_started_waitlist_card_points_only_its_owner_to_history(
    l8_state: DemoState, monkeypatch: pytest.MonkeyPatch
) -> None:
    alpha = booking.resolve_actor(l8_state, "fixture-fifo-alpha")
    outcome, state = booking.join_waitlist(l8_state, alpha, "workshop-1", now=NOW)
    assert outcome == "OK"
    row = state.registrations[-1]
    before = deepcopy(state)
    start = state.workshops[0].starts_at
    monkeypatch.setattr(booking, "server_now", lambda: start - timedelta(seconds=1))
    app = app_with_state(state)
    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-alpha").run()
    assert app.button(key="join_workshop-1").disabled
    card = rendered_workshop(app, "workshop-1")
    assert any("for your position" in item.value for item in card.get("caption"))

    monkeypatch.setattr(booking, "server_now", lambda: start)
    app.sidebar.button(key="refresh_view").click().run()
    card = rendered_workshop(app, "workshop-1")
    assert any(
        "Your waitlist entry is in Booking History." in item.value for item in card.get("caption")
    )
    assert not any("for your position" in item.value for item in card.get("caption"))
    assert app.button(key="join_workshop-1").disabled
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert len(app.dataframe) == 1
    history = app.dataframe[0].value
    assert list(history["Registration ID"]) == [row.registration_id]
    assert list(history["Status"]) == ["WAITLISTED"]
    assert "Position" not in history and not any(
        str(b.key).startswith("withdraw_") for b in app.button
    )

    app.sidebar.selectbox(key="selected_user_id").set_value("fixture-fifo-zulu").run()
    assert not app.dataframe
    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    card = rendered_workshop(app, "workshop-1")
    assert not any("Your waitlist entry" in item.value for item in card.get("caption"))
    assert app.button(key="join_workshop-1").disabled
    assert not app.exception and app.session_state.demo_state is state and state == before


def test_p2_fifo_fixture_has_two_distinct_test_only_participants(l8_state: DemoState) -> None:
    default = create_demo_state()
    assert l8_state.users == [
        *default.users,
        DemoUser("fixture-fifo-alpha", "FIFO Test Alpha", Role.PARTICIPANT),
        DemoUser("fixture-fifo-zulu", "FIFO Test Zulu", Role.PARTICIPANT),
    ]
    assert len({user.user_id for user in l8_state.users}) == 8
    assert resolve_actor(default, "fixture-fifo-alpha") is None
    assert resolve_actor(default, "fixture-fifo-zulu") is None


@pytest.mark.parametrize(
    ("user_id", "name"),
    [
        ("participant-1", "Xingjian"),
        ("participant-2", "Sam"),
        ("participant-leo", "Leo"),
        ("participant-willy", "Willy"),
    ],
)
def test_p2_all_default_participants_have_equal_permissions(
    workshop: Workshop, user_id: str, name: str
) -> None:
    state = create_demo_state()
    state.workshops = [workshop]
    state.next_workshop_id = 2
    actor = resolve_actor(state, user_id)
    other = resolve_actor(state, "participant-2" if user_id == "participant-1" else "participant-1")
    assert actor == DemoUser(user_id, name, Role.PARTICIPANT)
    assert check_permission(state, actor, Role.ORGANISER) == "FORBIDDEN"
    assert get_workshop_roster(state, actor, "workshop-1") == ("FORBIDDEN", ())
    assert booking.get_workshop_waitlist(state, actor, "workshop-1") == ("FORBIDDEN", ())
    before = deepcopy(state)
    outcome, booked = booking.book_workshop(state, actor, "workshop-1", now=NOW)
    assert outcome == "OK" and state == before
    record = Registration(
        "registration-1", "workshop-1", user_id, RegistrationStatus.CONFIRMED, NOW, NOW
    )
    assert booked == replace(before, registrations=[record], next_registration_id=2)
    assert booking.list_own_registrations(booked, actor) == ("OK", (record,))
    assert booking.list_own_registrations(booked, other) == ("OK", ())
    assert booking.cancel_registration(booked, other, "registration-1", now=NOW) == (
        "FORBIDDEN",
        booked,
    )
    assert booked == replace(before, registrations=[record], next_registration_id=2)


def test_p2_default_demo_promotes_leo_and_leaves_willy_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    original = deepcopy(app.session_state.demo_state)
    assert (original.next_workshop_id, original.next_registration_id) == (5, 5)
    assert not any(row.queue_seq is not None for row in original.registrations)
    assert [
        row.participant_id
        for row in original.registrations
        if row.workshop_id == "workshop-2" and row.status is RegistrationStatus.CONFIRMED
    ] == ["participant-2"]
    assert {row.participant_id for row in original.registrations} == {
        "participant-1",
        "participant-2",
    }

    for user_id, registration_id, position in (
        ("participant-leo", "registration-5", 1),
        ("participant-willy", "registration-6", 2),
    ):
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        app.sidebar.radio(key="current_view").set_value("Workshops").run()
        app.button(key="join_workshop-2").click().run()
        assert any(
            registration_id in message.value
            for message in rendered_workshop(app, "workshop-2").success
        )
        app.sidebar.radio(key="current_view").set_value("My Bookings").run()
        queue = app.dataframe[0].value
        assert list(queue["Registration ID"]) == [registration_id]
        assert list(queue["Position"]) == [position]
        assert list(queue["Status"]) == ["WAITLISTED"]

    queued = deepcopy(app.session_state.demo_state)
    assert queued.registrations[:4] == original.registrations
    assert queued.registrations[4:] == [
        Registration(
            "registration-5",
            "workshop-2",
            "participant-leo",
            RegistrationStatus.WAITLISTED,
            NOW,
            NOW,
            1,
        ),
        Registration(
            "registration-6",
            "workshop-2",
            "participant-willy",
            RegistrationStatus.WAITLISTED,
            NOW,
            NOW,
            2,
        ),
    ]
    assert (queued.next_workshop_id, queued.next_registration_id) == (5, 7)

    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-2"]
    decision = NOW + timedelta(minutes=1)
    monkeypatch.setattr(booking, "server_now", lambda: decision)
    app.button(key="cancel_registration-2").click().run()
    expected = [
        replace(row, status=RegistrationStatus.CANCELLED, updated_at=decision)
        if row.registration_id == "registration-2"
        else replace(row, status=RegistrationStatus.CONFIRMED, updated_at=decision)
        if row.registration_id == "registration-5"
        else row
        for row in queued.registrations
    ]
    assert app.session_state.demo_state == replace(queued, registrations=expected)

    app.sidebar.selectbox(key="selected_user_id").set_value("participant-leo").run()
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-5"]
    assert list(app.dataframe[0].value["Status"]) == ["CONFIRMED"]
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-willy").run()
    app.sidebar.button(key="refresh_view").click().run()
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-6"]
    assert list(app.dataframe[0].value["Position"]) == [1]
    assert list(app.dataframe[0].value["Status"]) == ["WAITLISTED"]

    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-2").run()
    app.sidebar.radio(key="current_view").set_value("Organiser").run()
    app.selectbox(key="roster_workshop_id").set_value("workshop-2").run()
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-5"]
    assert list(app.dataframe[0].value["Participant"]) == ["Leo"]
    assert list(app.dataframe[1].value["Registration ID"]) == ["registration-6"]
    assert list(app.dataframe[1].value["Participant"]) == ["Willy"]
    assert list(app.dataframe[1].value["Position"]) == [1]
    app.sidebar.selectbox(key="selected_user_id").set_value("organiser-1").run()
    assert all("workshop-2" not in item for item in app.selectbox(key="roster_workshop_id").options)
    final = app.session_state.demo_state
    rui = resolve_actor(final, "organiser-1")
    assert get_workshop_roster(final, rui, "workshop-2") == ("FORBIDDEN", ())
    assert booking.get_workshop_waitlist(final, rui, "workshop-2") == ("FORBIDDEN", ())
    assert final == replace(queued, registrations=expected)
    assert not app.exception


def test_p2_demo_guide_and_organiser_tabs_are_read_only() -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    original = deepcopy(app.session_state.demo_state)
    drafts = {
        "organiser-1": {"draft": {"new_title": "Rui draft"}},
        "organiser-2": {"draft": {"new_title": "Alex draft"}},
    }
    app.session_state.creation_forms = deepcopy(drafts)
    assert not app.expander
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-leo").run()
    assert [item.label for item in app.expander] == ["Booking & Waitlist Reminder"]
    reminder = app.expander[0]
    assert [item.type for item in reminder] == ["expander", "markdown"]
    assert "No automatic notifications." in reminder.markdown[0].value
    assert "Use Refresh view in My Bookings" in reminder.markdown[0].value
    assert app.session_state.creation_forms == drafts

    for organiser_id, saved_title, owned, foreign in (
        ("organiser-2", "Alex draft", "workshop-2", "workshop-1"),
        ("organiser-1", "Rui draft", "workshop-1", "workshop-2"),
    ):
        app.sidebar.selectbox(key="selected_user_id").set_value(organiser_id).run()
        app.sidebar.radio(key="current_view").set_value("Organiser").run()
        assert not app.expander
        assert [tab.label for tab in app.tabs] == ["Create Workshop", "Manage My Workshops"]
        assert app.tabs[0].button(key="create_workshop")
        assert app.tabs[0].text_input(key="new_title").value == saved_title
        options = app.tabs[1].selectbox(key="roster_workshop_id").options
        assert any(owned in option for option in options)
        assert all(foreign not in option for option in options)
        assert app.session_state.creation_forms == drafts
    assert app.session_state.demo_state == original
    assert not app.exception


def test_p2_default_waiter_can_withdraw_and_rejoin_without_leaking_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(booking, "server_now", lambda: NOW)
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    initial = deepcopy(app.session_state.demo_state)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-leo").run()
    stale_join = app.button(key="join_workshop-2")
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-willy")
    stale_join.click().run()
    assert any(
        "INVALID_ACTOR:" in message.value for message in rendered_workshop(app, "workshop-2").error
    )
    assert app.session_state.demo_state == initial
    app.button(key="join_workshop-2").click().run()
    joined = app.session_state.demo_state
    waiting = Registration(
        "registration-5",
        "workshop-2",
        "participant-willy",
        RegistrationStatus.WAITLISTED,
        NOW,
        NOW,
        1,
    )
    assert joined == replace(
        initial, registrations=[*initial.registrations, waiting], next_registration_id=6
    )

    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    app.button(key="withdraw_registration-5").click().run()
    withdrawn = replace(waiting, status=RegistrationStatus.CANCELLED)
    assert app.session_state.demo_state == replace(
        joined, registrations=[*initial.registrations, withdrawn]
    )
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-5"]
    assert list(app.dataframe[0].value["Status"]) == ["CANCELLED"]

    app.sidebar.radio(key="current_view").set_value("Workshops").run()
    app.button(key="join_workshop-2").click().run()
    rejoined = replace(waiting, registration_id="registration-6", queue_seq=2)
    expected = replace(
        initial,
        registrations=[*initial.registrations, withdrawn, rejoined],
        next_registration_id=7,
    )
    assert app.session_state.demo_state == expected
    app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    assert list(app.dataframe[0].value["Position"]) == [1]
    assert list(app.dataframe[0].value["Registration ID"]) == ["registration-6"]
    assert list(app.dataframe[1].value["Registration ID"]) == ["registration-5"]
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-leo").run()
    assert not app.dataframe and not app.exception
    assert app.session_state.demo_state == expected

    fresh = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert fresh.session_state.demo_state == initial
    assert fresh.session_state.demo_state is not app.session_state.demo_state
    assert fresh.sidebar.selectbox(key="selected_user_id").value is None


def test_p2_review_identity_switch_replaces_the_view_scope_without_changing_state() -> None:
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    original = deepcopy(app.session_state.demo_state)
    styles = None
    for actor_id, label, view in (
        ("organiser-2", "Alex (ORGANISER)", "Organiser"),
        ("organiser-1", "Rui Yan (ORGANISER)", "Organiser"),
        ("participant-2", "Sam (PARTICIPANT)", "My Bookings"),
    ):
        key = "identity_view_" + actor_id.encode().hex()
        app.sidebar.selectbox(key="selected_user_id").set_value(actor_id).run()
        app.sidebar.radio(key="current_view").set_value(view).run()
        assert [
            block.key
            for block in app.get("flex_container")
            if str(block.key).startswith("identity_view_")
        ] == [key]
        css = app.get("html")[0].proto.body
        assert f'[value="{label}"])) .st-key-{key}' in css
        assert "{ display: none; }" in css
        assert styles is None or css == styles
        styles = css
        assert app.session_state.demo_state == original
        assert not app.exception


def test_l9_near_cutoff_promotion_can_be_discovered_in_same_session_after_cutoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Keep the author walkthrough's calendar fixed and advance only this test's clock.
    start = datetime(2026, 12, 10, 9, tzinfo=WORKSHOP_TIMEZONE)
    cutoff = datetime(2026, 12, 9, 9, tzinfo=WORKSHOP_TIMEZONE)
    now = datetime(2026, 12, 6, 9, tzinfo=WORKSHOP_TIMEZONE)
    monkeypatch.setattr(booking, "server_now", lambda: now)
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    workshop = next(
        w for w in app.session_state.demo_state.workshops if w.workshop_id == "workshop-2"
    )
    assert (workshop.starts_at, workshop.registration_cutoff, workshop.capacity) == (
        start,
        cutoff,
        1,
    )

    for user_id, entry_id, position in (
        ("participant-leo", "registration-5", 1),
        ("participant-willy", "registration-6", 2),
    ):
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        app.sidebar.radio(key="current_view").set_value("Workshops").run()
        app.button(key="join_workshop-2").click().run()
        app.sidebar.radio(key="current_view").set_value("My Bookings").run()
        waiting = app.dataframe[0].value
        assert list(waiting["Registration ID"]) == [entry_id]
        assert list(waiting["Status"]) == ["WAITLISTED"]
        assert list(waiting["Position"]) == [position]
        assert any("There are no notifications." in notice.value for notice in app.caption)

    waiting_state = app.session_state.demo_state
    queued = deepcopy(waiting_state)
    now = cutoff - timedelta(minutes=1)

    stale_app = app_with_state(deepcopy(queued))
    stale_app.sidebar.selectbox(key="selected_user_id").set_value("participant-leo").run()
    stale_app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    stale_withdraw = stale_app.button(key="withdraw_registration-5")
    assert not stale_withdraw.disabled

    # A separate copy exercises a pre-C control submitted at C with both waiters active.
    cutoff_state = deepcopy(queued)
    cutoff_app = app_with_state(cutoff_state)
    cutoff_app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    cutoff_app.sidebar.radio(key="current_view").set_value("My Bookings").run()
    stale_cancel = cutoff_app.button(key="cancel_registration-2")
    assert not stale_cancel.disabled

    app.sidebar.selectbox(key="selected_user_id").set_value("participant-2").run()
    app.button(key="cancel_registration-2").click().run()
    changes = {
        "registration-2": RegistrationStatus.CANCELLED,
        "registration-5": RegistrationStatus.CONFIRMED,
    }
    expected = replace(
        queued,
        registrations=[
            replace(entry, status=changes[entry.registration_id], updated_at=now)
            if entry.registration_id in changes
            else entry
            for entry in queued.registrations
        ],
    )
    assert app.session_state.demo_state == expected
    assert [
        entry.registration_id
        for entry in app.session_state.demo_state.registrations
        if entry.workshop_id == "workshop-2" and entry.status is RegistrationStatus.CONFIRMED
    ] == ["registration-5"]
    assert waiting_state == queued

    now = cutoff
    stale_cancel.click().run()
    assert not cutoff_app.exception and not cutoff_app.success
    assert any("REGISTRATION_CLOSED" in error.value for error in cutoff_app.error)
    assert cutoff_app.button(key="cancel_registration-2").disabled
    assert cutoff_app.session_state.demo_state is cutoff_state and cutoff_state == queued

    # The participant first checks again after C, with the released seat already assigned.
    now = cutoff + timedelta(minutes=5)
    app.sidebar.selectbox(key="selected_user_id").set_value("participant-leo").run()
    app.sidebar.button(key="refresh_view").click().run()
    confirmed = app.dataframe[0].value
    assert list(confirmed["Registration ID"]) == ["registration-5"]
    assert list(confirmed["Status"]) == ["CONFIRMED"]
    assert list(confirmed["Registration cutoff"]) == ["2026-12-09 09:00:00 (Asia/Singapore)"]
    assert list(confirmed["Updated"]) == ["2026-12-09 08:59:00 (Asia/Singapore)"]
    assert app.button(key="cancel_registration-5").disabled
    promoted_state = app.session_state.demo_state
    assert promoted_state == expected

    # Keep this UI on the old render while its latest state already reflects promotion.
    latest = deepcopy(promoted_state)
    stale_app.session_state.demo_state = latest
    stale_withdraw.click().run()
    assert not stale_app.exception and not stale_app.success
    assert any("STATUS_CHANGED" in error.value for error in stale_app.error)
    assert stale_app.session_state.demo_state is latest and latest == expected

    willy = resolve_actor(promoted_state, "participant-willy")
    assert willy is not None
    outcome, same_state = booking.withdraw_waitlist(
        promoted_state, willy, "registration-5", now=now
    )
    assert outcome == "FORBIDDEN" and same_state is promoted_state and same_state == expected

    app.sidebar.selectbox(key="selected_user_id").set_value("participant-willy").run()
    still_waiting = app.dataframe[0].value
    assert list(still_waiting["Registration ID"]) == ["registration-6"]
    assert list(still_waiting["Status"]) == ["WAITLISTED"]
    assert list(still_waiting["Position"]) == [1]
    assert not app.button(key="withdraw_registration-6").disabled
    before_withdrawal = app.session_state.demo_state
    app.button(key="withdraw_registration-6").click().run()
    assert before_withdrawal == expected
    history = app.dataframe[0].value
    assert list(history["Registration ID"]) == ["registration-6"]
    assert list(history["Status"]) == ["CANCELLED"]
    assert app.session_state.demo_state == replace(
        expected,
        registrations=[
            replace(entry, status=RegistrationStatus.CANCELLED, updated_at=now)
            if entry.registration_id == "registration-6"
            else entry
            for entry in expected.registrations
        ],
    )
    assert not app.exception


@pytest.mark.parametrize(
    ("offset", "confirmed_hint", "waiting_hint", "cancel_open", "withdraw_open"),
    [
        (-1, "You may cancel before C", "FIFO promotion", True, True),
        (0, "cancellation deadline has passed", "Promotion closed at C", False, True),
        (86399, "cancellation deadline has passed", "Promotion closed at C", False, True),
        (86400, "Check Booking History", "Check Booking History", False, False),
        (86401, "Check Booking History", "Check Booking History", False, False),
    ],
    ids=["before-C", "at-C", "before-S", "at-S", "after-S"],
)
def test_l9_status_guidance_respects_confirmed_and_waiting_boundaries(
    monkeypatch: pytest.MonkeyPatch,
    offset: int,
    confirmed_hint: str,
    waiting_hint: str,
    cancel_open: bool,
    withdraw_open: bool,
) -> None:
    state = create_demo_data(NOW)
    state.registrations.append(
        Registration(
            "registration-5",
            "workshop-2",
            "participant-leo",
            RegistrationStatus.WAITLISTED,
            NOW,
            NOW,
            1,
        )
    )
    state.next_registration_id = 6
    baseline = deepcopy(state)
    cutoff = datetime(2026, 12, 4, 9, tzinfo=WORKSHOP_TIMEZONE)
    monkeypatch.setattr(booking, "server_now", lambda: cutoff + timedelta(seconds=offset))
    app = app_with_state(state)

    for user_id, reg_id, status, hint, action, action_open in (
        ("participant-2", "registration-2", "CONFIRMED", confirmed_hint, "cancel", cancel_open),
        (
            "participant-leo",
            "registration-5",
            "WAITLISTED",
            waiting_hint,
            "withdraw",
            withdraw_open,
        ),
    ):
        app.sidebar.selectbox(key="selected_user_id").set_value(user_id).run()
        app.sidebar.radio(key="current_view").set_value("Workshops").run()
        card = rendered_workshop(app, "workshop-2")
        assert any(hint in caption.value for caption in card.get("caption"))
        assert any("Confirmed bookings: 1" in caption.value for caption in card.get("caption"))
        summary = app.metric[1]
        assert summary.label == "Confirmed bookings in this session"
        assert any("do not measure attendance" in caption.value for caption in app.caption)
        app.sidebar.radio(key="current_view").set_value("My Bookings").run()
        app.sidebar.button(key="refresh_view").click().run()
        assert any(
            "Outdoor Photography Walk" in caption.value and hint in caption.value
            for caption in app.caption
        )
        controls = {button.key: button for button in app.button}
        button_key = f"{action}_{reg_id}"
        if withdraw_open:
            assert button_key in controls and (not controls[button_key].disabled) == action_open
        else:
            assert button_key not in controls
        rows = [
            record
            for table in app.dataframe
            for record in table.value.to_dict("records")
            if record["Registration ID"] == reg_id
        ]
        assert len(rows) == 1 and rows[0]["Status"] == status
        if status == "WAITLISTED" and not withdraw_open:
            assert rows[0]["Waitlist"] == "Closed at workshop start"
            assert "Position" not in rows[0]
        assert not app.exception and app.session_state.demo_state is state and state == baseline
