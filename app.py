"""V1.0 candidate: workshop creation, booking, cancellation, history and owned rosters."""

from datetime import UTC, datetime, time, timedelta

import streamlit as st

from booking import (
    WORKSHOP_TIMEZONE,
    DemoState,
    DemoUser,
    RegistrationStatus,
    Role,
    book_workshop,
    browse_workshops,
    cancel_registration,
    check_permission,
    confirmed_count,
    create_demo_data,
    create_workshop,
    get_workshop_roster,
    list_own_registrations,
    list_owned_workshops,
    resolve_actor,
    server_now,
    workshop_creation_errors,
)


def format_instant(value: datetime) -> str:
    return value.astimezone(WORKSHOP_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S") + " (Asia/Singapore)"


def show_workshops(state: DemoState, now: datetime, actor: DemoUser | None) -> None:
    st.info("Browse workshops below. Times are shown in Asia/Singapore.")
    message = st.session_state.pop("booking_message", None)
    if message and actor is not None and message[0] == actor.user_id:
        st.success(message[1])
    workshops = browse_workshops(state)
    if not workshops:
        st.write("No workshops have been created in this session.")
    for workshop in workshops:
        confirmed = confirmed_count(state, workshop.workshop_id)
        with st.container(border=True):
            st.markdown(f"**{workshop.title}**")
            st.caption(workshop.workshop_id)
            st.write("Start:", format_instant(workshop.starts_at))
            st.write("End:", format_instant(workshop.ends_at))
            st.write("Registration cutoff:", format_instant(workshop.registration_cutoff))
            st.write("Meeting point:", workshop.location)
            st.write(
                "Preparation:", workshop.preparation_notes or "No additional preparation notes."
            )
            st.write(
                f"Capacity: {workshop.capacity} | Confirmed: {confirmed} | "
                f"Remaining: {workshop.capacity - confirmed}"
            )
            if now >= workshop.starts_at:
                st.caption("Started - historical information.")
            elif now >= workshop.registration_cutoff:
                st.caption("Confirmed roster locked: booking is closed under the 24-hour policy.")
            else:
                st.caption("Registration window open. Availability is shown in the counts above.")
            if actor is not None and actor.role == Role.PARTICIPANT:
                if st.button(
                    "Book workshop",
                    key=f"book_{workshop.workshop_id}",
                    disabled=now >= workshop.registration_cutoff,
                    help="Booking requires a free place, no active duplicate and an open window.",
                ):
                    outcome, candidate = book_workshop(
                        state, actor, workshop.workshop_id, now=server_now()
                    )
                    if outcome == "OK":
                        registration = candidate.registrations[-1]
                        st.session_state.demo_state = candidate
                        st.session_state.booking_message = (
                            actor.user_id,
                            f"Booked {workshop.title}: {registration.registration_id} (CONFIRMED).",
                        )
                        st.rerun()
                    else:
                        explanations = {
                            "INVALID_ACTOR": "Select a valid participant demo identity.",
                            "FORBIDDEN": "Only participants may book workshops.",
                            "UNKNOWN_WORKSHOP": "This workshop is no longer available.",
                            "INVALID_INPUT": "The server time is unavailable. Please try again.",
                            "REGISTRATION_CLOSED": "Booking closed 24 hours before the start.",
                            "DUPLICATE_ACTIVE": "You already have a confirmed booking for this workshop.",
                            "FULL": "No places remain. Waitlisting is not available in this release.",
                        }
                        st.error(
                            f"{outcome}: {explanations.get(outcome, 'Booking is unavailable.')}"
                        )


def show_my_bookings(state: DemoState, actor: DemoUser, now: datetime) -> None:
    st.info("View your confirmed bookings and retained history for the selected demo identity.")
    outcome, registrations = list_own_registrations(state, actor)
    if outcome != "OK":
        st.error("Your booking records are unavailable. Refresh and try again.")
        return
    message = st.session_state.pop("cancellation_message", None)
    if message and message[0] == actor.user_id:
        st.success(message[1])
    workshops = {workshop.workshop_id: workshop for workshop in state.workshops}
    current, history = [], []
    for record in registrations:
        workshop = workshops[record.workshop_id]
        row = {
            "Registration ID": record.registration_id,
            "Workshop ID": record.workshop_id,
            "Workshop": workshop.title,
            "Status": record.status.value,
            "Start": format_instant(workshop.starts_at),
            "End": format_instant(workshop.ends_at),
            "Registration cutoff": format_instant(workshop.registration_cutoff),
            "Meeting point": workshop.location,
            "Created": format_instant(record.created_at),
            "Updated": format_instant(record.updated_at),
        }
        if record.status == RegistrationStatus.CONFIRMED and now.astimezone(
            UTC
        ) < workshop.starts_at.astimezone(UTC):
            current.append(row)
        else:
            history.append(row)
    for title, rows in (("Upcoming confirmed bookings", current), ("History", history)):
        st.subheader(title)
        if rows:
            st.dataframe(rows, hide_index=True, width="stretch")
        else:
            st.write("No records in this section for the selected identity.")
    confirmed = [r for r in registrations if r.status == RegistrationStatus.CONFIRMED]
    if confirmed:
        st.subheader("Cancel a confirmed booking")
        for record in confirmed:
            workshop = workshops[record.workshop_id]
            if st.button(
                f"Cancel {record.registration_id}: {workshop.title}",
                key=f"cancel_{record.registration_id}",
                disabled=now.astimezone(UTC) >= workshop.registration_cutoff.astimezone(UTC),
                help="Only the owner may cancel, strictly before the 24-hour cutoff.",
            ):
                outcome, candidate = cancel_registration(
                    state, actor, record.registration_id, now=server_now()
                )
                if outcome == "OK":
                    st.session_state.demo_state = candidate
                    st.session_state.cancellation_message = (
                        actor.user_id,
                        f"Cancelled {record.registration_id}: {workshop.title}. "
                        "One place released; the registration remains in History.",
                    )
                    st.rerun()
                elif outcome == "ALREADY_CANCELLED":
                    st.info(
                        "ALREADY_CANCELLED: This record is already cancelled; no further place released."
                    )
                else:
                    explanations = {
                        "INVALID_ACTOR": "Select a valid participant demo identity.",
                        "FORBIDDEN": "Only participants may cancel their own bookings.",
                        "UNKNOWN_REGISTRATION": "This registration is no longer available.",
                        "UNKNOWN_WORKSHOP": "This workshop is no longer available.",
                        "INVALID_INPUT": "The server time is unavailable. Please try again.",
                        "REGISTRATION_CLOSED": "Confirmed cancellation closed 24 hours before the start.",
                    }
                    st.error(
                        f"{outcome}: {explanations.get(outcome, 'Cancellation is unavailable.')}"
                    )
    st.caption(
        "History includes cancelled records and started workshops; original statuses are retained. "
        "Cancel only your own confirmed booking before its 24-hour cutoff."
    )


def show_organiser(state: DemoState, actor: DemoUser) -> None:
    st.info("Create workshops and view confirmed rosters for your own workshops.")
    default_day = server_now().astimezone(WORKSHOP_TIMEZONE).date() + timedelta(days=3)
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
    creation, rosters = st.columns(2)
    with creation:
        st.markdown("#### Create a workshop")
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
        st.markdown("#### My workshops and confirmed rosters")
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
        st.caption(f"Confirmed participants: {len(registrations)}")
        st.caption("Only confirmed participants are listed; cancelled history consumes no place.")
        if not registrations:
            st.write("No confirmed participants for this workshop.")
        else:
            names = {user.user_id: user.display_name for user in state.users}
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


def main() -> None:
    st.set_page_config(page_title="Outdoor Workshop Booking", page_icon="🌿", layout="wide")

    if "demo_state" not in st.session_state:
        st.session_state.demo_state = create_demo_data(server_now())
    state = st.session_state.demo_state

    st.title("Outdoor Workshop Booking and Waitlist Management System")
    st.caption(
        "V1.0 candidate: book workshops, cancel your confirmed bookings and retain your history."
    )
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
        if actor is not None:
            st.caption(f"Selected: {actor.display_name} | Role: {actor.role}")
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
        st.caption("Demo identity selection is not secure login. Use fictional data only.")

    workshops, confirmed = st.columns(2)
    workshops.metric("Workshop records in this session", len(state.workshops))
    confirmed.metric(
        "Confirmed records in this session",
        sum(record.status == RegistrationStatus.CONFIRMED for record in state.registrations),
    )

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

    st.markdown("**Registration policy**")
    st.write(
        "Workshops must be created more than 24 hours before their start. "
        "Booking and confirmed cancellation close 24 hours before the start. "
        "The later waitlist release will allow withdrawal until the workshop starts, "
        "while joining and promotion close at the 24-hour cutoff."
    )
    st.caption("Workshop times will be displayed in Asia/Singapore.")


if __name__ == "__main__":
    main()
