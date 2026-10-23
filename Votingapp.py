"""Streamlit entry point: python -m streamlit run Votingapp.py.

The interface collects input and displays results. Validation and state changes
live in project_app2.py; optional local-chain calls live in blockchain.py.
"""

from dataclasses import asdict

import streamlit as st

from project_app2 import CANDIDATES, DemoVotingService, VotingError, load_employees

DEMO_MODE = "Demo (no blockchain)"
BLOCKCHAIN_MODE = "Local blockchain (legacy)"


def get_service(mode: str, employees):
    """Keep demo state per browser session, never in a global shared cache."""
    if mode == DEMO_MODE:
        if "demo_service" not in st.session_state:
            st.session_state.demo_service = DemoVotingService(employees)
        return st.session_state.demo_service
    # Optional dependencies are imported only when this mode is selected.
    try:
        from blockchain import create_blockchain_service
    except ImportError as error:
        raise VotingError(
            "Install optional dependencies: python -m pip install -r requirements-blockchain.txt"
        ) from error
    if "blockchain_service" not in st.session_state:
        st.session_state.blockchain_service = create_blockchain_service(employees)
    return st.session_state.blockchain_service


def show_candidates() -> None:
    """Render the same candidate definitions used by the ballot and results."""
    st.header("Meet the candidates")
    for column, candidate in zip(st.columns(len(CANDIDATES)), CANDIDATES):
        with column:
            if candidate.image.is_file():
                st.image(str(candidate.image), width=150)
            st.subheader(candidate.name)
            st.write(candidate.bio)


def main() -> None:
    """Render registration, voting, and results with explicit success/error paths."""
    st.set_page_config(page_title="Board Member Voting Demo", page_icon="🗳️", layout="wide")
    st.title("Board Member Voting Demo")
    st.write(
        "Explore employee registration, voting tokens, and candidate results with sample data."
    )
    mode = st.sidebar.radio("Mode", [DEMO_MODE, BLOCKCHAIN_MODE], key="mode")
    if mode == DEMO_MODE:
        st.info("Demo votes exist only in this browser session. Use the sample details below.")
        if st.sidebar.button("Reset demo", key="reset_demo"):
            st.session_state.pop("demo_service", None)
            st.session_state.pop("demo_token", None)
    else:
        st.warning(
            "Legacy local-chain prototype: repeat voting is not prevented by the contract, "
            "and registration fields are public on-chain. Use only disposable test data."
        )
        if st.sidebar.button("Reconnect local node", key="reconnect"):
            st.session_state.pop("blockchain_service", None)
            st.session_state.pop("blockchain_token", None)
    try:
        employees = load_employees()
        service = get_service(mode, employees)
    except VotingError as error:
        st.error(str(error))
        st.stop()
    with st.expander("Sample employees — use these fictional details"):
        st.table([asdict(employee) for employee in employees])
        st.caption(
            "The four-digit demo suffix is fictional. Do not enter a real SSN or real employee data."
        )
    show_candidates()

    st.header("1. Register a sample employee")
    with st.form("registration_form"):
        name = st.text_input("Name", key="employee_name")
        phone = st.text_input("Phone number", key="employee_phone")
        suffix = st.text_input("Demo SSN suffix (4 digits)", max_chars=4, key="employee_suffix")
        employee_id = st.text_input("Employee ID", key="employee_id")
        registered = st.form_submit_button("Register", key="register")
    if registered:
        try:
            with st.spinner("Registering..."):
                token_id = service.register_voter(name, phone, suffix, employee_id)
        except VotingError as error:
            st.error(str(error))
        else:
            st.session_state["demo_token" if mode == DEMO_MODE else "blockchain_token"] = token_id
            st.success(f"Registration successful. Your token ID is {token_id}.")

    st.header("2. Cast a vote")
    last_token = st.session_state.get("demo_token" if mode == DEMO_MODE else "blockchain_token")
    if last_token is not None:
        st.caption(f"Most recently registered token in this mode: {last_token}")
    with st.form("voting_form"):
        # Text avoids floating-point precision loss for Solidity uint256 IDs.
        token_text = st.text_input("Token ID", value="0", key="vote_token")
        candidate_index = st.selectbox(
            "Choose a candidate",
            range(len(CANDIDATES)),
            format_func=lambda index: CANDIDATES[index].name,
            key="vote_candidate",
        )
        voted = st.form_submit_button("Vote", key="vote")
    if voted:
        try:
            token_text = token_text.strip()
            if not token_text.isascii() or not token_text.isdigit() or len(token_text) > 78:
                raise VotingError("Token ID must contain only digits (up to 78).")
            with st.spinner("Recording vote..."):
                transaction_hash = service.cast_vote(int(token_text), candidate_index)
        except VotingError as error:
            st.error(str(error))
        else:
            st.success("Vote recorded successfully.")
            if transaction_hash:
                st.code(transaction_hash, language=None)

    st.header("3. View results")
    # A button causes a rerun; results are then read after any vote above.
    st.button("Refresh results", key="refresh_results")
    try:
        results = service.view_results()
    except VotingError as error:
        st.error(str(error))
    else:
        st.table(
            [
                {"Candidate": candidate.name, "Votes": count}
                for candidate, count in zip(CANDIDATES, results)
            ]
        )


if __name__ == "__main__":
    main()
