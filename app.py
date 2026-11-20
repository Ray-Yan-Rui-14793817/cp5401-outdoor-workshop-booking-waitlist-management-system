"""Workshop booking and waitlist candidate for CR-01."""

import json
import platform
import re
from datetime import UTC, datetime, time, timedelta
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import streamlit as st

import booking
from booking import (
    WORKSHOP_TIMEZONE,
    DemoState,
    DemoUser,
    RegistrationStatus,
    Role,
    browse_workshops,
    check_permission,
    confirmed_count,
    create_demo_data,
    create_workshop,
    get_workshop_roster,
    get_workshop_waitlist,
    list_own_registrations,
    list_own_waitlist_positions,
    list_owned_workshops,
    resolve_actor,
    server_now,
    workshop_creation_errors,
)


def runtime_identity(root: Path) -> dict:
    """Read source/Git/package provenance; absent metadata is explicitly unknown."""
    sources = {}
    requirements = ""
    for name in ("app.py", "booking.py", "requirements.txt"):
        try:
            raw = (root / name).read_bytes()
        except OSError:
            sources[name] = None
        else:
            sources[name] = sha256(raw).hexdigest()
            if name == "requirements.txt":
                requirements = raw.decode("utf-8")
    commit = None
    try:
        head = (root / ".git/HEAD").read_text(encoding="utf-8").strip()
        if head.startswith("ref: "):
            head = (root / ".git" / head[5:]).read_text(encoding="utf-8").strip()
        if re.fullmatch(r"[0-9a-f]{40}", head):
            commit = head
    except OSError:
        pass
    packages = {}
    for name in re.findall(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]+\])?==", requirements, re.M):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = None
    return {
        "git_sha": commit,
        "python": platform.python_version(),
        "source_sha256": sources,
        "runtime_packages": packages,
    }


def format_instant(value: datetime) -> str:
    return value.astimezone(WORKSHOP_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S") + " (Asia/Singapore)"


STARTED_BOOKING_GUIDANCE = (
    "This workshop has started. Check Booking History for the recorded status. "
    "Booking, cancellation and waitlist actions are closed."
)


def active_booking_guidance(status: RegistrationStatus, closed: bool) -> str:
    if status == RegistrationStatus.WAITLISTED:
        if closed:
            return (
                "WAITLISTED is unconfirmed. Promotion closed at C. "
                "You may withdraw before the workshop starts (S)."
            )
        return (
            "WAITLISTED means unconfirmed. Use Refresh view regularly before C to check for "
            "FIFO promotion. There are no notifications. You may withdraw before S, "
            "including during the final 24 hours."
        )
    if closed:
        return "Your booking is confirmed. The cancellation deadline has passed. Review your booking details."
    return (
        "Your booking is confirmed. Review the meeting point and preparation notes. "
        "You may cancel before C if your plans change."
    )


def show_booking_reminder() -> None:
    with st.expander("Booking & Waitlist Reminder"):
        st.markdown(
            "**Before C.** Check My Bookings regularly, especially near the registration cutoff "
            "(C). WAITLISTED means unconfirmed. FIFO promotion may occur before C. "
            "Review the workshop details and plan ahead.\n\n"
            "**From C.** Use Refresh view in My Bookings to check your status. New bookings, "
            "waitlist joining, promotion and confirmed cancellation are closed. "
            "Waiting entries can still be withdrawn before the workshop starts (S).\n\n"
            "**No automatic notifications.** Consider setting your own reminder to check before C."
        )


def show_refusal(outcome: str) -> None:
    if outcome == "ALREADY_CANCELLED":
        st.info("ALREADY_CANCELLED: This record is already cancelled. Check Booking History.")
        return
    explanations = {
        "INVALID_ACTOR": "Check the selected demo identity and try again.",
        "FORBIDDEN": "This action is unavailable to the selected identity.",
        "UNKNOWN_WORKSHOP": "Refresh the view to see available workshops.",
        "UNKNOWN_REGISTRATION": "Refresh the view to see your registrations.",
        "INVALID_INPUT": "The server time is unavailable. Please try again.",
        "REGISTRATION_CLOSED": "The 24-hour registration cutoff has passed. Refresh the view for current options.",
        "WORKSHOP_STARTED": "The workshop has started. Find the registration in Booking History.",
        "DUPLICATE_ACTIVE": "You already have an active registration. Open My Bookings to check its status.",
        "FULL": "No places remain. Select Join Waitlist to request a place.",
        "USE_BOOKING": "A place is available. Select Book workshop.",
        "INTEGRITY_ERROR": "Availability conflicts with the queue. Refresh the view and try again.",
        "STATUS_CHANGED": "Refresh the view and check your current registration status.",
    }
    st.error(f"{outcome}: {explanations.get(outcome, 'Refresh the view and try again.')}")


def book_from_view(workshop_id: str, rendered_user_id: str) -> None:
    state = st.session_state.demo_state
    selected_id = st.session_state.get("selected_user_id")
    if selected_id != rendered_user_id:
        st.session_state.book_feedback = (selected_id, workshop_id, "INVALID_ACTOR", None)
        return
    actor = resolve_actor(state, selected_id)
    outcome, candidate = booking.book_workshop(state, actor, workshop_id, now=booking.server_now())
    registration_id = None
    if outcome == "OK":
        registration_id = candidate.registrations[-1].registration_id
        st.session_state.demo_state = candidate
    st.session_state.book_feedback = (selected_id, workshop_id, outcome, registration_id)


def join_from_view(workshop_id: str, rendered_user_id: str) -> None:
    # Handle the original click before rendering hides a now-ineligible control.
    state = st.session_state.demo_state
    selected_id = st.session_state.get("selected_user_id")
    if selected_id != rendered_user_id:
        st.session_state.join_feedback = (selected_id, workshop_id, "INVALID_ACTOR", None)
        return
    actor = resolve_actor(state, selected_id)
    outcome, candidate = booking.join_waitlist(state, actor, workshop_id, now=booking.server_now())
    registration_id = None
    if outcome == "OK":
        registration_id = candidate.registrations[-1].registration_id
        st.session_state.demo_state = candidate
    st.session_state.join_feedback = (selected_id, workshop_id, outcome, registration_id)


def show_workshops(state: DemoState, now: datetime, actor: DemoUser | None) -> None:
    now = now.astimezone(UTC)
    st.info("Browse workshops below. Times are shown in Asia/Singapore.")
    selected_id = actor.user_id if actor is not None else None
    active_by_workshop = {}
    if actor is not None and actor.role == Role.PARTICIPANT:
        outcome, registrations = list_own_registrations(state, actor)
        if outcome == "OK":
            active_by_workshop = {
                row.workshop_id: row.status
                for row in registrations
                if row.status in (RegistrationStatus.CONFIRMED, RegistrationStatus.WAITLISTED)
            }
    book_feedback = st.session_state.pop("book_feedback", None)
    if book_feedback and book_feedback[0] != selected_id:
        book_feedback = None
    join_feedback = st.session_state.pop("join_feedback", None)
    if join_feedback and join_feedback[0] != selected_id:
        join_feedback = None
    workshops = browse_workshops(state)
    for feedback in (book_feedback, join_feedback):
        if feedback and not any(w.workshop_id == feedback[1] for w in workshops):
            show_refusal(feedback[2])
    if not workshops:
        st.write("No workshops have been created in this session.")
    for workshop in workshops:
        confirmed = confirmed_count(state, workshop.workshop_id)
        remaining = workshop.capacity - confirmed
        full = remaining <= 0
        active_status = active_by_workshop.get(workshop.workshop_id)
        cutoff = workshop.registration_cutoff
        closed = now >= cutoff
        started = now >= workshop.starts_at
        with st.container(border=True, key=f"workshop_card_{workshop.workshop_id}"):
            st.markdown(f"### {workshop.title}")
            if started:
                st.badge("STARTED", color="grey")
            elif closed:
                st.badge("BOOKING CLOSED", color="blue")
            elif full:
                st.badge("FULL / WAITLIST OPEN", color="orange")
            else:
                st.badge("BOOKING OPEN", color="green")
            st.caption(f"Workshop ID {workshop.workshop_id}")
            schedule, availability = st.columns([2, 1])
            with schedule:
                st.write("**Start (S):**", format_instant(workshop.starts_at))
                st.write("**Registration cutoff (C):**", format_instant(cutoff))
                st.write("End:", format_instant(workshop.ends_at))
            with availability:
                st.write(f"**Remaining places: {remaining}**")
                st.caption(f"Capacity: {workshop.capacity} | Confirmed bookings: {confirmed}")
                st.write("**Meeting point:**", workshop.location)
            st.write(
                "Preparation:", workshop.preparation_notes or "No additional preparation notes."
            )
            if actor is not None and actor.role == Role.PARTICIPANT:
                if active_status is not None:
                    if started:
                        history_hint = (
                            "Your waitlist entry is in Booking History. "
                            if active_status == RegistrationStatus.WAITLISTED
                            else ""
                        )
                        st.caption(history_hint + STARTED_BOOKING_GUIDANCE)
                    else:
                        own_entry = (
                            "You are already on this waitlist. Open My Bookings for your position. "
                            if active_status == RegistrationStatus.WAITLISTED
                            else "You already have a confirmed booking for this workshop. "
                        )
                        st.caption(own_entry + active_booking_guidance(active_status, closed))
                elif full and not closed:
                    st.caption(
                        "WAITLISTED means unconfirmed. FIFO promotion may occur before C. "
                        "Check My Bookings for updates. There are no notifications."
                    )
                with st.container(horizontal=True):
                    st.button(
                        "Book workshop",
                        key=f"book_{workshop.workshop_id}",
                        disabled=closed,
                        type="secondary" if full else "primary",
                        on_click=book_from_view,
                        args=(workshop.workshop_id, actor.user_id),
                    )
                    if full:
                        st.button(
                            "Join Waitlist",
                            key=f"join_{workshop.workshop_id}",
                            disabled=closed or active_status is not None,
                            type="primary",
                            on_click=join_from_view,
                            args=(workshop.workshop_id, actor.user_id),
                        )
            if book_feedback and book_feedback[1] == workshop.workshop_id:
                _, _, result, registration_id = book_feedback
                if result == "OK":
                    st.success(
                        f"Booked {workshop.title}: {registration_id} (CONFIRMED). "
                        "Open My Bookings for details."
                    )
                else:
                    show_refusal(result)
            if join_feedback and join_feedback[1] == workshop.workshop_id:
                _, _, result, registration_id = join_feedback
                if result == "OK":
                    st.success(
                        f"Joined the waitlist (WAITLISTED). Registration ID: {registration_id}. "
                        "Open My Bookings for your position and status."
                    )
                else:
                    show_refusal(result)


def cancel_from_view(registration_id: str, workshop_id: str) -> None:
    state = st.session_state.demo_state
    selected_id = st.session_state.get("selected_user_id")
    actor = resolve_actor(state, selected_id)
    outcome, candidate = booking.cancel_registration(
        state, actor, registration_id, now=booking.server_now()
    )
    message = ""
    if outcome == "OK":
        waiting_ids = {
            row.registration_id
            for row in state.registrations
            if row.workshop_id == workshop_id and row.status == RegistrationStatus.WAITLISTED
        }
        promoted = any(
            row.registration_id in waiting_ids and row.status == RegistrationStatus.CONFIRMED
            for row in candidate.registrations
        )
        result = "One waiting participant was promoted." if promoted else "One place released."
        message = f"Cancelled {registration_id}. {result} Find the record in Booking History."
        st.session_state.demo_state = candidate
    st.session_state.cancellation_feedback = (selected_id, outcome, message)


def withdraw_from_view(registration_id: str) -> None:
    # Streamlit calls this before rerendering, so a stale click retains Withdraw intent.
    state = st.session_state.demo_state
    selected_id = st.session_state.get("selected_user_id")
    actor = resolve_actor(state, selected_id)
    outcome, candidate = booking.withdraw_waitlist(
        state, actor, registration_id, now=booking.server_now()
    )
    if outcome == "OK":
        st.session_state.demo_state = candidate
    st.session_state.withdrawal_feedback = (selected_id, outcome)


def show_my_bookings(state: DemoState, actor: DemoUser, now: datetime) -> None:
    now = now.astimezone(UTC)
    st.info("View confirmed bookings, waiting entries and history for the selected demo identity.")
    outcome, registrations = list_own_registrations(state, actor)
    if outcome != "OK":
        st.error("Your booking records are unavailable. Refresh and try again.")
        return
    cancellation = st.session_state.pop("cancellation_feedback", None)
    if cancellation and cancellation[0] == actor.user_id:
        if cancellation[1] == "OK":
            st.success(cancellation[2])
        else:
            show_refusal(cancellation[1])
    feedback = st.session_state.pop("withdrawal_feedback", None)
    if feedback and feedback[0] == actor.user_id:
        result = feedback[1]
        if result == "OK":
            st.success("Withdrawn from the waitlist. Find the record in Booking History.")
        else:
            show_refusal(result)
    workshops = {workshop.workshop_id: workshop for workshop in state.workshops}
    _, positions = list_own_waitlist_positions(state, actor)
    current, waiting, history = [], [], []
    for record in registrations:
        workshop = workshops[record.workshop_id]
        started = now >= workshop.starts_at
        row = {
            "Workshop": workshop.title,
            "Status": record.status.value,
            "Registration ID": record.registration_id,
        }
        if record.status == RegistrationStatus.WAITLISTED:
            if started:
                row["Waitlist"] = "Closed at workshop start"
            else:
                row["Position"] = positions[record.registration_id]
        row.update(
            {
                "Start": format_instant(workshop.starts_at),
                "Registration cutoff": format_instant(workshop.registration_cutoff),
                "Meeting point": workshop.location,
                "End": format_instant(workshop.ends_at),
                "Workshop ID": record.workshop_id,
                "Created": format_instant(record.created_at),
                "Updated": format_instant(record.updated_at),
            }
        )
        if record.status == RegistrationStatus.CONFIRMED and not started:
            current.append(row)
        elif record.status == RegistrationStatus.WAITLISTED and not started:
            waiting.append(row)
        else:
            history.append(row)

    with st.container(border=True):
        st.subheader("Upcoming Confirmed Bookings")
        if current:
            st.dataframe(current, hide_index=True, width="stretch")
            for row in current:
                registration_id = row["Registration ID"]
                workshop = workshops[row["Workshop ID"]]
                closed = now >= workshop.registration_cutoff
                st.caption(
                    f"{workshop.title}. {active_booking_guidance(RegistrationStatus.CONFIRMED, closed)}"
                )
                st.button(
                    f"Cancel Booking: {workshop.title} ({registration_id})",
                    key=f"cancel_{registration_id}",
                    disabled=closed,
                    on_click=cancel_from_view,
                    args=(registration_id, workshop.workshop_id),
                )
        else:
            st.write("No upcoming confirmed bookings.")

    with st.container(border=True):
        st.subheader("My Waitlist")
        if waiting:
            st.dataframe(waiting, hide_index=True, width="stretch")
            for row in waiting:
                registration_id = row["Registration ID"]
                workshop = workshops[row["Workshop ID"]]
                closed = now >= workshop.registration_cutoff
                st.caption(
                    f"{workshop.title}. {active_booking_guidance(RegistrationStatus.WAITLISTED, closed)}"
                )
                st.button(
                    f"Withdraw Waitlist: {row['Workshop']} ({registration_id})",
                    key=f"withdraw_{registration_id}",
                    on_click=withdraw_from_view,
                    args=(registration_id,),
                )
        else:
            st.write("No active waitlist entries.")

    with st.container(border=True):
        st.subheader("Booking History")
        if history:
            st.dataframe(history, hide_index=True, width="stretch")
            for row in history:
                workshop = workshops[row["Workshop ID"]]
                if now >= workshop.starts_at:
                    st.caption(f"{workshop.title}. {STARTED_BOOKING_GUIDANCE}")
        else:
            st.write("No booking history.")


def show_organiser(state: DemoState, actor: DemoUser) -> None:
    st.info("Create workshops and view confirmed rosters for your own workshops.")
    display_now = server_now()
    default_day = display_now.astimezone(WORKSHOP_TIMEZONE).date() + timedelta(days=3)
    defaults = {
        "new_title": "",
        "new_start_date": default_day,
        "new_start_time": time(9),
        "new_end_date": default_day,
        "new_end_time": time(12),
        "new_location": "",
        "new_capacity": 10,
        "new_notes": "",
    }
    forms = st.session_state.setdefault("creation_forms", {})
    form = forms.setdefault(actor.user_id, {})
    reset = form.pop("reset", False)
    # The shared widget keys display only the selected organiser's form.
    changed_organiser = st.session_state.get("creation_form_owner") != actor.user_id
    draft = form.get("draft", {})
    for key, value in defaults.items():
        if reset or changed_organiser or key not in st.session_state:
            st.session_state[key] = value if reset else draft.get(key, value)
    st.session_state.creation_form_owner = actor.user_id
    errors = form.get("errors", {})

    def show_field_error(field: str) -> None:
        if field in errors:
            st.error(errors[field])

    message = form.pop("message", None)
    if message:
        st.success(message)
    creation, rosters = st.tabs(["Create Workshop", "Manage My Workshops"])
    with creation:
        if form.get("feedback"):
            st.error(form["feedback"])
        with st.form("create_workshop_form", clear_on_submit=False):
            title = st.text_input("Title", key="new_title")
            show_field_error("title")
            starts_date = st.date_input(
                "Start date (Asia/Singapore)",
                value=None,
                format="YYYY-MM-DD",
                key="new_start_date",
            )
            starts_time = st.time_input("Start time", value=None, step=60, key="new_start_time")
            show_field_error("starts_at")
            ends_date = st.date_input(
                "End date (Asia/Singapore)",
                value=None,
                format="YYYY-MM-DD",
                key="new_end_date",
            )
            ends_time = st.time_input("End time", value=None, step=60, key="new_end_time")
            show_field_error("ends_at")
            location = st.text_input("Meeting point", key="new_location")
            show_field_error("location")
            capacity = st.number_input(
                "Capacity",
                value=None,
                step=1,
                key="new_capacity",
                help="Enter a whole number from 1 to 30.",
            )
            show_field_error("capacity")
            notes = st.text_area("Preparation notes (optional)", key="new_notes")
            show_field_error("preparation_notes")
            submitted = st.form_submit_button(
                "Create workshop", key="create_workshop", type="primary"
            )
        st.caption(
            "Creation requires more than 24 hours of notice at submission, including seconds."
        )
        show_field_error("now")
        if submitted:
            fields = {
                "title": title,
                "starts_at": (
                    datetime.combine(starts_date, starts_time, tzinfo=WORKSHOP_TIMEZONE)
                    if starts_date is not None and starts_time is not None
                    else None
                ),
                "ends_at": (
                    datetime.combine(ends_date, ends_time, tzinfo=WORKSHOP_TIMEZONE)
                    if ends_date is not None and ends_time is not None
                    else None
                ),
                "location": location,
                "capacity": capacity,
                "preparation_notes": notes,
                "now": server_now(),
            }
            outcome, candidate = create_workshop(state, actor, **fields)
            if outcome == "OK":
                created = candidate.workshops[-1]
                st.session_state.demo_state = candidate
                st.session_state.roster_workshop_id = created.workshop_id
                forms[actor.user_id] = {
                    "message": f"Created {created.workshop_id}: {created.title}.",
                    "reset": True,
                }
                st.rerun()
            else:
                forms[actor.user_id] = {
                    "draft": {
                        "new_title": title,
                        "new_start_date": starts_date,
                        "new_start_time": starts_time,
                        "new_end_date": ends_date,
                        "new_end_time": ends_time,
                        "new_location": location,
                        "new_capacity": capacity,
                        "new_notes": notes,
                    },
                    "errors": (
                        workshop_creation_errors(**fields) if outcome == "INVALID_INPUT" else {}
                    ),
                    "feedback": {
                        "INVALID_INPUT": (
                            "Workshop not created. Your entries have been kept. "
                            "Correct the highlighted fields and submit again."
                        ),
                        "INVALID_ACTOR": "INVALID_ACTOR: Select a valid demo identity.",
                        "FORBIDDEN": "FORBIDDEN: Only organisers may create workshops.",
                    }.get(
                        outcome, "Workshop creation is unavailable. Your entries have been kept."
                    ),
                }
                st.rerun()

    with rosters:
        outcome, workshops = list_owned_workshops(state, actor)
        if outcome != "OK":
            st.error("Your workshop list is unavailable. Refresh and try again.")
            return
        if not workshops:
            st.write("You have no workshops in this session.")
            return
        labels = {w.workshop_id: f"{w.title} ({w.workshop_id})" for w in workshops}
        if st.session_state.get("roster_workshop_id") not in labels:
            st.session_state.roster_workshop_id = next(iter(labels))
        target_id = st.selectbox(
            "Your workshop",
            options=list(labels),
            format_func=lambda workshop_id: labels[workshop_id],
            key="roster_workshop_id",
        )
        outcome, registrations = get_workshop_roster(state, actor, target_id)
        if outcome != "OK":
            st.error(f"{outcome}: The confirmed roster is unavailable for this identity.")
            return
        target = next(workshop for workshop in workshops if workshop.workshop_id == target_id)
        st.subheader("Confirmed Roster")
        st.caption(
            f"Capacity: {target.capacity} | Remaining places: {target.capacity - len(registrations)}"
        )
        st.caption(f"Confirmed bookings: {len(registrations)}")
        st.caption("This roster shows confirmed bookings. Cancelled records use no places.")
        names = {user.user_id: user.display_name for user in state.users}
        if not registrations:
            st.write("No confirmed bookings for this workshop.")
        else:
            st.dataframe(
                [
                    {
                        "Registration ID": row.registration_id,
                        "Participant ID": row.participant_id,
                        "Participant": names.get(row.participant_id, row.participant_id),
                        "Status": row.status.value,
                    }
                    for row in registrations
                ],
                hide_index=True,
                width="stretch",
            )
        outcome, waiters = get_workshop_waitlist(state, actor, target_id)
        if outcome != "OK":
            st.error(f"{outcome}: The waitlist is unavailable for this identity.")
            return
        st.subheader("Workshop Waitlist")
        closed = display_now >= target.starts_at
        if closed:
            st.caption("Waitlist closed at workshop start. Remaining entries are historical.")
        if not waiters:
            st.write("No waiting participants for this workshop.")
        else:
            st.dataframe(
                [
                    {
                        ("Queue order at close" if closed else "Position"): position,
                        "Registration ID": row.registration_id,
                        "Participant ID": row.participant_id,
                        "Participant": names.get(row.participant_id, row.participant_id),
                        "Status": row.status.value,
                    }
                    for position, row in enumerate(waiters, start=1)
                ],
                hide_index=True,
                width="stretch",
            )


def identity_view_key(user_id: str | None) -> str:
    return "identity_view_" + (user_id.encode().hex() if user_id is not None else "guest")


def hide_other_identity_views(identity_labels: dict[str | None, str]) -> None:
    """Hide prior identity content as soon as the browser selection changes."""
    control = '[data-testid="stSidebar"] input[aria-label="Select demo identity"]'
    selectors = []
    for user_id, label in identity_labels.items():
        # Escape CSS strings and prevent the label from ending the style element.
        value = "".join(
            f"\\{ord(char):x} " if char in '<"\\' or ord(char) < 32 else char for char in label
        )
        key = identity_view_key(user_id)
        selectors.append(f'body:not(:has({control}[value="{value}"])) .st-key-{key}')
    st.html("<style>" + ",\n".join(selectors) + " { display: none; }</style>")


def main() -> None:
    st.set_page_config(page_title="Outdoor Workshop Booking", page_icon="🌿", layout="wide")

    if not st.session_state.get("_runtime_identity_logged"):
        print(
            "L6_RUNTIME_IDENTITY "
            + json.dumps(runtime_identity(Path(__file__).parent), sort_keys=True),
            flush=True,
        )
        st.session_state._runtime_identity_logged = True

    if "demo_state" not in st.session_state:
        st.session_state.demo_state = create_demo_data(server_now())
    state = st.session_state.demo_state

    required_roles = {"My Bookings": Role.PARTICIPANT, "Organiser": Role.ORGANISER}

    with st.sidebar:
        st.header("Demo identity")
        identity_labels = {None: "No demo identity selected"}
        identity_labels.update(
            {user.user_id: f"{user.display_name} ({user.role})" for user in state.users}
        )
        selected_id = st.selectbox(
            "Select demo identity",
            options=list(identity_labels),
            format_func=lambda user_id: identity_labels[user_id],
            key="selected_user_id",
        )
        actor = resolve_actor(state, selected_id)
        st.header("Explore")
        visible_views = ["Workshops"]
        if actor is not None:
            visible_views.extend(
                view for view, role in required_roles.items() if actor.role == role
            )
        if st.session_state.get("current_view") not in visible_views:
            st.session_state.current_view = "Workshops"
        view = st.radio("View", visible_views, key="current_view")
        st.button("Refresh view", key="refresh_view")
        st.info(
            "This teaching prototype uses temporary data in one browser session. "
            "Other sessions do not share it. Browser reload or server restart may reset it."
        )

    hide_other_identity_views(identity_labels)
    st.title("Outdoor Workshop Booking and Waitlist Management System")
    if actor is None:
        st.badge("Fictional identity: None selected", color="grey")
    else:
        st.badge(f"Fictional identity: {actor.display_name} | Role: {actor.role}", color="blue")
    st.caption("Demo identity selection is not secure authentication. Use fictional data only.")
    workshops, confirmed = st.columns(2)
    workshops.metric("Workshop records in this session", len(state.workshops))
    confirmed.metric(
        "Confirmed bookings in this session",
        sum(record.status == RegistrationStatus.CONFIRMED for record in state.registrations),
    )

    st.caption("Booking counts show reserved places and do not measure attendance.")

    st.markdown("**Registration policy**")
    st.write(
        "The registration cutoff (C) is 24 elapsed hours before the workshop start (S). "
        "Booking, confirmed cancellation, waitlist joining and automatic promotion close at C. "
        "A waiting entry can be withdrawn until S."
    )

    with st.container(key=identity_view_key(selected_id)):
        if actor is not None and actor.role == Role.PARTICIPANT:
            show_booking_reminder()
        st.subheader(view)
        if view not in ("Workshops", "My Bookings", "Organiser"):
            st.error("This view is unavailable. Please refresh and try again.")
        elif view == "Workshops":
            show_workshops(state, server_now(), actor)
        else:
            required_role = required_roles[view]
            permission = check_permission(state, actor, required_role)
            if permission == "INVALID_ACTOR":
                st.warning("Select a demo identity to use this view.")
            elif permission == "FORBIDDEN":
                st.warning(f"This view is available to {required_role.value.lower()}s only.")
            elif permission == "OK":
                if view == "Organiser":
                    show_organiser(state, actor)
                else:
                    show_my_bookings(state, actor, server_now())
            else:
                st.error("This view is unavailable. Please refresh and try again.")


if __name__ == "__main__":
    main()
