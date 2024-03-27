# Import required modules and functions
#Import necessary modules and functions from project_app2
import streamlit as st
from project_app2 import register_voter, cast_vote, view_results, get_candidates
import time

# Set up the web interface using Streamlit
#Create the main title for the voting system web page
st.title("Company Board Member Voting System")


# Timer and Results Viewing (Sidebar)
#If "Start Timer" button is clicked in sidebar:
    #Start a countdown timer for 60 minutes
if st.sidebar.button("Start Timer"):
    end_time = time.time() + 60 * 60 
    st.session_state['end_time'] = end_time
else:
    end_time = st.session_state.get('end_time', None)

if end_time:
    remaining_time = int(end_time - time.time())
    if remaining_time > 0:
        st.sidebar.write(f"Time Remaining: {remaining_time} seconds")
    else:
        st.sidebar.write("Voting ended")


if st.sidebar.button("View Current Results"):
    results = view_results()
    for i, candidate in enumerate(["Alice", "Bob", "Charlie", "Diana"]):
        st.write(f"{candidate}: {results[i]} votes")


# Display Candidate Information
#Retrieve and display information about the candidates
get_candidates()


# Voter Registration Form
#Create a form for voter registration with fields for name, phone number, SSN, and employee ID
st.header("Voter Registration")
with st.form("registration_form"):
    name = st.text_input("Name")
    phoneNumber = st.number_input("Phone Number",value=0)
    ssnLast4 = st.number_input("Last 4 digits of SSN",value=0)
    employeeId = st.number_input("Employee ID",value=0)
    submitted = st.form_submit_button("Register")
    #If the registration form is submitted:
    #Attempt to register the voter
    #Display success or error message based on the registration attempt
    if submitted:
        try:
            registration_response = register_voter(name, phoneNumber, ssnLast4, employeeId)
            st.write(registration_response)
            st.success("Voter registered successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")


# Casting Vote Form
#Create a form for casting votes with fields for token ID and candidate selection
st.header("Cast Your Vote")
with st.form("voting_form"):
    tokenId = st.number_input("Token ID",value=0)
    candidate_index = st.selectbox("Choose a candidate", [0, 1, 2, 3], format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x])
    vote_submitted = st.form_submit_button("Vote")

    if vote_submitted:
        try:
            voting_token_id = cast_vote(tokenId, candidate_index)
            st.success("Vote cast successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")




