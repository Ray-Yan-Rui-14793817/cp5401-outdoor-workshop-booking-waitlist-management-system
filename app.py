"""Streamlit shell for L1; role and booking operations follow in later loops."""

import streamlit as st

from booking import RegistrationStatus, create_demo_state


def main() -> None:
    st.set_page_config(page_title="Outdoor Workshop Booking", page_icon="🌿", layout="wide")

    if "demo_state" not in st.session_state:
        st.session_state.demo_state = create_demo_state()
    state = st.session_state.demo_state

    st.title("Outdoor Workshop Booking and Waitlist Management System")
    st.caption("Development preview: booking and organiser actions are not yet available.")

    with st.sidebar:
        st.header("Explore")
        view = st.radio("View", ("Workshops", "My Bookings", "Organiser"), key="current_view")
        st.button("Refresh view", key="refresh_view")
        st.info(
            "This teaching prototype uses temporary data in one browser session. "
            "Other sessions do not share it. Browser reload or server restart may reset it."
        )
        st.caption("Use fictional data only. Planned demo identity selection is not secure login.")

    workshops, confirmed = st.columns(2)
    workshops.metric("Workshop records in this session", len(state.workshops))
    confirmed.metric(
        "Confirmed records in this session",
        sum(record.status == RegistrationStatus.CONFIRMED for record in state.registrations),
    )

    st.subheader(view)
    messages = {
        "Workshops": "Workshop browsing is not yet available in this preview.",
        "My Bookings": "Participant selection and booking actions are not yet available.",
        "Organiser": "Workshop creation and organiser rosters are not yet available.",
    }
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
