# Import required modules and set up environment
#Import necessary modules and load environment variables
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from web3.exceptions import ContractLogicError

load_dotenv()


# Establish a connection to the blockchain using Web3
#Connect to the Web3 provider using the provided URI
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Load and set up the smart contract
@st.cache_resource
def load_contract():
    # Load Contract ABI
    with open(Path('./contracts/compiled/project_3.json')) as f:
        project_abi = json.load(f)
    #Connect to the deployed contract on the blockchain
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


# Define a function to verify if a person is an employee
def verify_employee(name, phoneNumber, ssnLast4, employeeId):
    return any(
        (employees['name'] == name) &
        (employees['phone_number'] == phoneNumber) &
        (employees['Last_4_SSN'] == ssnLast4) &
        (employees['employee_id'] == employeeId)
    )


# Voter Registration Function
def register_voter(name, phoneNumber, ssnLast4, employeeId):
    #Verify if the person is an employee
    if verify_employee(name, phoneNumber, ssnLast4, employeeId):
        try:
            # Create a transaction to register the voter
            tx = contract.functions.register_voter(name, phoneNumber, ssnLast4, employeeId).transact({
                'from': w3.eth.accounts[0],
                'gas': 1000000 
            })
            tokenId = contract.functions.totalTokens().call() - 1
            return tokenId
        except ContractLogicError as e:
            # This catches the revert from the Solidity contract
            return f"Registration failed: {e}"
    else:
        return "Employee verification failed."


# Voting Function
def cast_vote(tokenId, candidate_index):
    #Create a blockchain transaction to record the vote
    tx = contract.functions.vote(tokenId, candidate_index).transact({
        'from': w3.eth.accounts[0],
        'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
    })

# Create a function to visulize reults
def view_results():
    #Define a function to retrieve voting results from the blockchain
    results = contract.functions.viewResults().call()
    return results


 
#Create a dictionary containing detailed information about each candidate
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


# Create a function that will display the candidates 
def get_candidates():
    """Display the database of candidate information."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        st.image(db_list[number][2], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Bio: ", db_list[number][1])
        st.text(" \n")
