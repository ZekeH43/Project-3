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
    with open(Path('./contracts/compiled/projectvote.json')) as f:
        project_abi = json.load(f)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    return w3.eth.contract(address=contract_address, abi=project_abi)

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
        private_key = os.getenv("PRIVATE_KEY")
        tx = contract.functions.registerVoter(name, phone, ssn_last4, employee_id).buildTransaction({
            'from': w3.eth.accounts[0],
            'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0]),
            'gas': 1000000
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Assuming the event log is indexed correctly, and the first log entry is what we need
        token_id = tx_receipt.logs[0].args.tokenId if tx_receipt.logs else None
        return token_id if token_id is not None else "Registration failed or token ID not found."
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
