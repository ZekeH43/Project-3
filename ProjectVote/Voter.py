import streamlit as st
from project_app3 import register_voter, cast_vote, view_results
import time

st.title("Company Board Member Voting System")

# Start Timer
if st.sidebar.button("Start Timer", key="start_timer_key"):
    end_time = time.time() + 60 * 60  # 1 hour from now
    st.session_state['end_time'] = end_time
else:
    end_time = st.session_state.get('end_time', None)

# Display the remaining time
if end_time:
    remaining_time = int(end_time - time.time())
    if remaining_time > 0:
        st.sidebar.write(f"Time Remaining: {remaining_time} seconds")
    else:
        st.sidebar.write("Voting ended")

# View Results
if st.sidebar.button("View Current Results", key="view_results_button"):
    results = view_results()
    for i, candidate in enumerate(["Alice", "Bob", "Charlie", "Diana"]):
        st.write(f"{candidate}: {results[i]} votes")

# Voter Registration Form
st.header("Voter Registration")
with st.form("registration_form"):
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    ssn_last4 = st.text_input("Last 4 digits of SSN")
    employee_id = st.text_input("Employee ID")
    submitted = st.form_submit_button("Register")
    if submitted:
        token_id = register_voter(name, phone, ssn_last4, employee_id)
        if isinstance(token_id, int):
            st.success(f"Voter registered successfully! Your token ID is {token_id}.")
        else:
            st.error(f"Registration failed: {token_id}")


# Voting Form
st.header("Cast Your Vote")
with st.form("voting_form"):
    token_id = st.text_input("Your Token ID", key="vote_token_id")
    candidate_index = st.selectbox(
        "Choose a candidate", 
        [0, 1, 2, 3], 
        format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x], 
        key="vote_candidate"
    )
    vote_submitted = st.form_submit_button("Vote")  # Removed the 'key' argument
    if vote_submitted:
        try:
            voting_response = cast_vote(int(token_id), candidate_index)
            st.success("Vote cast successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
