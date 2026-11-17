"""L3 workshop browsing, creation and owned confirmed rosters."""

from datetime import datetime, time, timedelta

import streamlit as st

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
    list_owned_workshops,
    resolve_actor,
    server_now,
)


def format_instant(value: datetime) -> str:
    return value.astimezone(WORKSHOP_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S") + " (Asia/Singapore)"


def show_workshops(state: DemoState, now: datetime) -> None:
    st.info("Browse workshops below. Times are shown in Asia/Singapore.")
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
                st.caption("Registration window open. Booking actions arrive in a later loop.")


def show_organiser(state: DemoState, actor: DemoUser) -> None:
    st.info("Create workshops and view confirmed rosters for your own workshops.")
    message = st.session_state.pop("creation_message", None)
    if message:
        st.success(message)
    creation, rosters = st.columns(2)
    with creation:
        st.markdown("#### Create a workshop")
        default_day = server_now().astimezone(WORKSHOP_TIMEZONE).date() + timedelta(days=3)
        with st.form("create_workshop_form", clear_on_submit=True):
            title = st.text_input("Title", key="new_title")
            starts_date = st.date_input(
                "Start date (Asia/Singapore)",
                value=default_day,
                format="YYYY-MM-DD",
                key="new_start_date",
            )
            starts_time = st.time_input("Start time", value=time(9), step=60, key="new_start_time")
            ends_date = st.date_input(
                "End date (Asia/Singapore)",
                value=default_day,
                format="YYYY-MM-DD",
                key="new_end_date",
            )
            ends_time = st.time_input("End time", value=time(12), step=60, key="new_end_time")
            location = st.text_input("Meeting point", key="new_location")
            capacity = st.number_input(
                "Capacity", min_value=1, max_value=30, value=10, step=1, key="new_capacity"
            )
            notes = st.text_area("Preparation notes (optional)", key="new_notes")
            submitted = st.form_submit_button(
                "Create workshop", key="create_workshop", type="primary"
            )
        st.caption(
            "Creation requires more than 24 hours of notice at submission, including seconds."
        )
        if submitted:
            outcome, candidate = create_workshop(
                state,
                actor,
                title=title,
                starts_at=(
                    datetime.combine(starts_date, starts_time, tzinfo=WORKSHOP_TIMEZONE)
                    if starts_date is not None and starts_time is not None
                    else None
                ),
                ends_at=(
                    datetime.combine(ends_date, ends_time, tzinfo=WORKSHOP_TIMEZONE)
                    if ends_date is not None and ends_time is not None
                    else None
                ),
                location=location,
                capacity=capacity,
                preparation_notes=notes,
                now=server_now(),
            )
            if outcome == "OK":
                created = candidate.workshops[-1]
                st.session_state.demo_state = candidate
                st.session_state.roster_workshop_id = created.workshop_id
                st.session_state.creation_message = (
                    f"Created {created.workshop_id}: {created.title}."
                )
                st.rerun()
            else:
                st.error(
                    {
                        "INVALID_INPUT": (
                            "INVALID_INPUT: Use a title, meeting point, capacity 1-30, an end "
                            "after the start, and a start more than 24 hours from submission."
                        ),
                        "INVALID_ACTOR": "INVALID_ACTOR: Select a valid demo identity.",
                        "FORBIDDEN": "FORBIDDEN: Only organisers may create workshops.",
                    }.get(outcome, "Workshop creation is unavailable. Refresh and try again.")
                )

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
        "L3 preview: browse and create workshops. Booking and cancellation follow in later loops."
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
        show_workshops(state, server_now())
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
                st.info("Booking actions and personal history will be added in later loops.")
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
