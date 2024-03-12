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
@st.cache_resource
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

# converting from float to int
employees['employee_id'] = employees['employee_id'].astype(object)

# converting from float to int
employees['Last_4_SSN'] = employees['Last_4_SSN'].astype(object)

def verify_employee(name, phoneNumber, ssnLast4, employeeId):
    return any(
        (employees['name'] == name) &
        (employees['phone_number'] == phoneNumber) &
        (employees['Last_4_SSN'] == ssnLast4) &
        (employees['employee_id'] == employeeId)
    )

def register_voter(name, phoneNumber, ssnLast4, employeeId):
    if verify_employee(name, phoneNumber, ssnLast4, employeeId):
        # Create a transaction to register the voter
        tx = contract.functions.register_voter(name, phoneNumber, ssnLast4, employeeId).transact({
            'from': w3.eth.accounts[0],
            #'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0]),
            'gas': 1000000 
        })

        # Sign the transaction
        #signed_tx = w3.eth.account.signTransaction(tx)

        # Send the transaction
        #tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Wait for the transaction receipt
        #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Assume the token ID is the total number of tokens issued so far
        tokenId = contract.functions.totalTokens().call() - 1

        return tokenId
    else:
        return "Employee verification failed."

def cast_vote(tokenId, candidate_index):
    tx = contract.functions.vote(tokenId, candidate_index).buildTransaction({
        'from': w3.eth.accounts[0],
        'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
    })
    #signed_tx = w3.eth.account.signTransaction(tx)
    #tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #token_event = tx_receipt['logs'][0]
    #tokenId = w3.toInt(hexstr=token_event['data'])

    #candidate_index = st.selectbox("Choose a candidate", [0, 1, 2, 3], format_func=lambda x: ["Alice", "Bob", "Charlie", "Diana"][x])
    #vote_submitted = st.form_submit_button("Vote")
    #if vote_submitted:
        #try:
            #voting_response = cast_vote(tokenId, candidate_index)
            #st.success("Vote cast successfully!")
        #except Exception as e:
            #st.error(f"An error occurred: {e}")

def view_results():
    results = contract.functions.viewResults().call()
    return results


candidate_database = {
    "Alice": [
        "Alice",
        "With a passion for both the great outdoors and cutting-edge technology, Alice is an avid hiker who finds solace in nature while leveraging her expertise in crafting computer chips.",
        "Images/Alice.jpg",
    ],
    "Bob": [
        "Bob",
        " Balancing his love for culinary adventures with a rewarding career in computer chip manufacturing, Bob is a dedicated foodie constantly seeking new flavors and experiences both in the kitchen and the lab.",
        "Images/Bob.jpg",
    ],
    "Charlie": [
        "Charlie",
        "An enthusiast of melodic tunes and computer chip design alike, Charlie immerses himself in music and guitar-playing while pursuing his profession in the captivating world of chip fabrication.",
        "Images/Charlie.jpg",
    ],
    "Diana": [
        "Diana",
        "Combining her love for literature with a successful career in computer chip engineering, Diana is a passionate reader who explores diverse literary worlds alongside her endeavors in cutting-edge technology.",
        "Images/Diana.jpg",
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
        st.write("Bio: ", db_list[number][1])
        st.text(" \n")
