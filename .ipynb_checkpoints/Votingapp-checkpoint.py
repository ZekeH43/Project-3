#Imports
import streamlit as st
from project_app2 import register_voter, cast_vote, view_results
import time

st.title("Company Board Member Voting System")

# Timer (Simplified for performance)
if st.sidebar.button("Start Timer"):
    end_time = time.time() + 60*60
    st.session_state['end_time'] = end_time
else:
    end_time = st.session_state.get('end_time', None)

if end_time:
    remaining_time = int(end_time - time.time())
    if remaining_time > 0:
        st.sidebar.write(f"Time Remaining: {remaining_time} seconds")
    else:
        st.sidebar.write("Voting ended")

# View Results
if st.sidebar.button("View Current Results"):
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
        try:
            registration_response = register_voter(name, phone, ssn_last4, employee_id)
            st.success("Voter registered successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Voting Form
st.header("Cast Your Vote")
with st.form("voting_form"):
    token_id = st.text_input("Your Token ID")
    candidate_index = st.selectbox("Choose a candidate", [0, 1, 2, 3], format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x])
    vote_submitted = st.form_submit_button("Vote")
    if vote_submitted:
        try:
            voting_response = cast_vote(token_id, candidate_index)
            st.success("Vote cast successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
