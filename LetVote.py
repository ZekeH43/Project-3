#Imports
import streamlit as st
from projectapp import register_voter, cast_vote, view_results
import time

# Assuming you've set up the functions register_voter, cast_vote, view_results in your_backend_script

st.title("Company Board Member Voting System")

# Placeholder for the voting timer
timer = st.sidebar.empty()
end_time = time.time() + 60*60 
while time.time() < end_time:
    timer.write(f"Time Remaining: {int(end_time - time.time())} seconds")
    time.sleep(1)

if st.sidebar.button("View Current Results"):
    results = view_results()
    for i, candidate in enumerate(["Alice", "Bob", "Charlie", "Diana"]):
        st.write(f"{candidate}: {results[i]} votes")

st.header("Voter Registration")
with st.form("registration_form"):
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    ssn_last4 = st.text_input("Last 4 digits of SSN")
    employee_id = st.text_input("Employee ID")
    submitted = st.form_submit_button("Register")
    if submitted:
        registration_response = register_voter(name, phone, ssn_last4, employee_id)
        st.write(registration_response)
        
st.header("Cast Your Vote")
with st.form("voting_form"):
    token_id = st.text_input("Your Token ID")
    candidate_index = st.selectbox("Choose a candidate", [0, 1, 2, 3], format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x])
    vote_submitted = st.form_submit_button("Vote")
    if vote_submitted:
        voting_response = cast_vote(token_id, candidate_index)
        st.write(voting_response)



