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

# Contract Helper function:
@st.cache(allow_output_mutation=True)
def load_contract():
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
        (employees['employee_ID'] == employee_id)
    )

def register_voter(name, phone, ssn_last4, employee_id):
    if verify_employee(name, phone, ssn_last4, employee_id):
        # Create a transaction to register the voter
        tx = contract.functions.registerVoter(name, phone, ssn_last4, employee_id).buildTransaction({
            'from': w3.eth.accounts[0],  # The account that sends the transaction
            'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
        })

        # Sign and send the transaction
        signed_tx = w3.eth.account.signTransaction(tx, 'your_private_key')  # Replace with your private key
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt
    else:
        return "Employee verification failed."

# Streamlit interface for Voter Registration
st.header("Voter Registration")
with st.form("registration_form"):
    input_name = st.text_input("Name")
    input_phone = st.text_input("Phone Number")
    input_ssn_last4 = st.text_input("Last 4 Digits of SSN")
    input_employee_id = st.text_input("Employee ID")
    submitted = st.form_submit_button("Register")

    if submitted:
        register_response = register_voter(input_name, input_phone, input_ssn_last4, input_employee_id)
        if isinstance(register_response, str):
            st.error(register_response)
        else:
            st.success("Voter registered successfully!")
