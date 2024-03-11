#Load Imports
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd


load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache_resource()
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/project_3.json')) as f:
        project_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=project_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()



def register_voter(name, phone, ssn_last4, employee_id):
    if verify_employee(name, phone, ssn_last4, employee_id):
        # Create a transaction to register the voter
        tx = contract.functions.registerVoter(name, phone, ssn_last4, employee_id).buildTransaction({
            'from': web3.eth.accounts[0],  # The account that sends the transaction
            'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])
        })

        # Sign the transaction (replace 'your_private_key' with the actual private key)
        signed_tx = web3.eth.account.signTransaction(tx, 'your_private_key')

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Get transaction receipt (optional, to confirm it was mined)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt
    else:
        return "Employee verification failed."

def cast_vote(token_id, candidate_index):
    # Create a transaction to cast a vote
    tx = contract.functions.vote(token_id, candidate_index).buildTransaction({
        'from': web3.eth.accounts[0],
        'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])
    })

    signed_tx = web3.eth.account.signTransaction(tx, 'your_private_key')
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

def view_results():
    # Call the contract to view results
    results = contract.functions.viewResults().call()
    return results

# Load your employee dataset
employees = pd.read_csv('fake_employee.csv')


def verify_employee(name, phone, ssn_last4, employee_id):
    return any(
        (employees['name'] == name) &
        (employees['phone_number'] == phone) &
        (employees['Last_4_SSN'] == ssn_last4) &
        (employees['employee_ID'] == employee_id)
    )




project_app2
def cast_vote(token_id, candidate_index):
    private_key = os.getenv("PRIVATE_KEY")
    tx = contract.functions.vote(token_id, candidate_index).buildTransaction({
        'from': w3.eth.accounts[0],
        'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
    })
    signed_tx = w3.eth.account.signTransaction(tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt





Votingapp
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




def get_candidates():
    """Display the database of candidate information."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Bio: ", db_list[number][2])
        st.text(" \n")







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
            voting_token_id = cast_vote(token_id, candidate_index)
            st.success("Vote cast successfully! Your voting token ID is: {}".format(voting_token_id))
        except Exception as e:
            st.error(f"An error occurred: {e}")





candidate_database = {
    "Alice": [
        "Alice",
        "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0",
        "Images/Alice.jpeg",
    ],
    "Bob": [
        "Bob",
        "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396",
        "Images/Bob.jpeg",
    ],
    "Charlie": [
        "Charlie",
        "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45",
        "Images/Charlie.jpeg",
    ],
    "Diana": [
        "Diana",
        "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45",
        "Images/Diana.jpeg",
    ],
}


# A list of the candidates first names
people = ["Alice", "Bob", "Charlie", "Diana"]


def get_candidates():
    """Display the database of candidate information."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        # Correct index for image
        st.image(db_list[number][2], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Bio: ", db_list[number][?])
        st.text(" \n")

get_candidates()








# Voting Form
st.header("Cast Your Vote")
with st.form("voting_form"):
    st.header("Cast Your Vote")
with st.form("voting_form"):
    token_id = st.text_input("Your Token ID")
    candidate_index = st.selectbox("Choose a candidate", [0, 1, 2, 3], format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x])
    vote_submitted = st.form_submit_button("Vote")
    if vote_submitted:
        try:
            voting_token_id = cast_vote(token_id, candidate_index)
            st.success("Vote cast successfully! Your voting token ID is: {}".format(voting_token_id))
        except Exception as e:
            st.error(f"An error occurred: {e}")
