# Load Imports
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

# Load the contract
@st.cache(allow_output_mutation=True)
def load_contract():
    # Load Contract ABI
    with open(Path('./contracts/compiled/project_3.json')) as f:
        project_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = w3.eth.contract(address=contract_address, abi=project_abi)
    return contract

contract = load_contract()

# Load your employee dataset
employees = pd.read_csv('fake_employee.csv')

def verify_employee(name, phone, ssn_last4, employee_id):
    return any(
        (employees['name'] == name) &
        (employees['phone_number'] == phone) &
        (employees['Last_4_SSN'] == ssn_last4) &
        (employees['employee_id'] == employee_id)
    )

def register_voter(name, phone, ssn_last4, employee_id):
    if verify_employee(name, phone, ssn_last4, employee_id):
        # Create a transaction to register the voter
        tx = contract.functions.registerVoter(name, phone, ssn_last4, employee_id).buildTransaction({
            'from': w3.eth.accounts[0],  # The account that sends the transaction
            'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0]),
            'gas': 1000000 
        })

        # Sign the transaction using the private key
        private_key = os.getenv("PRIVATE_KEY")
        signed_tx = w3.eth.account.signTransaction(tx, private_key)

        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Wait for the transaction receipt
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Assume the token ID is the total number of tokens issued so far
        token_id = contract.functions.totalTokens().call() - 1

        return token_id
    else:
        return "Employee verification failed."

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

def view_results():
    results = contract.functions.viewResults().call()
    return results

    candidate_index = st.selectbox("Choose a candidate", [0, 1, 2, 3], format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x])
    vote_submitted = st.form_submit_button("Vote")
    if vote_submitted:
        try:
            voting_response = cast_vote(token_id, candidate_index)
            st.success("Vote cast successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
