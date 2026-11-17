"""L2 demo identity selection and role-gated preview views."""

import streamlit as st

from booking import RegistrationStatus, Role, check_permission, create_demo_state, resolve_actor


def main() -> None:
    st.set_page_config(page_title="Outdoor Workshop Booking", page_icon="🌿", layout="wide")

    if "demo_state" not in st.session_state:
        st.session_state.demo_state = create_demo_state()
    state = st.session_state.demo_state

    st.title("Outdoor Workshop Booking and Waitlist Management System")
    st.caption("Development preview: workshop and booking actions will be added later.")

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
        view = st.radio("View", ("Workshops", "My Bookings", "Organiser"), key="current_view")
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
    messages = {
        "Workshops": "Workshop browsing is not yet available in this preview.",
        "My Bookings": "Booking actions and personal history will be added in later loops.",
        "Organiser": "Workshop creation and organiser rosters are not yet available.",
    }
    required_role = {"My Bookings": Role.PARTICIPANT, "Organiser": Role.ORGANISER}.get(view)
    if required_role is None:
        st.info(messages[view])
    else:
        permission = check_permission(state, actor, required_role)
        if permission == "INVALID_ACTOR":
            st.warning("Select a demo identity to use this view.")
        elif permission == "FORBIDDEN":
            st.warning(f"This view is available to {required_role.value.lower()}s only.")
        else:
            st.info(messages[view])

    st.markdown("**Planned registration policy**")
    st.write(
        "Workshops must be created more than 24 hours before their start. "
        "Booking and confirmed cancellation close 24 hours before the start. "
        "The later waitlist release will allow withdrawal until the workshop starts, "
        "while joining and promotion close at the 24-hour cutoff."
    )
    st.caption("Workshop times will be displayed in Asia/Singapore.")


if __name__ == "__main__":
    main()
