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