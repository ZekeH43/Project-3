# Tech Company Board Member Voting System

## Overview

-We are creating a voting system for a tech company to cast votes on who they want to be added as a board member. This system is designed to ensure a transparent and secure voting process using blockchain technology and a user-friendly interface.

## Instructions
The instructions for this project are divided into the following steps:

### Step 1: Create the Smart Contract in Solidity

The smart contract VotingSystem is written in Solidity and includes the following key components:

##### 1. Solidity Version and OpenZeppelin Import:
Specifies Solidity version ^0.5.5.
Imports ERC721Full from OpenZeppelin, a standard for non-fungible tokens (NFTs), to represent voting tokens.

##### 2.Contract Declaration:
The VotingSystem contract inherits from ERC721Full, indicating each voter will have a unique token.

##### 3.Voter Structure:
Defines a Voter struct to store a voter's name, phone number, the last four digits of their SSN, and employee ID.

##### 4.State Variables:
-voters: A mapping from token IDs to Voter structs, storing voter information.

-registeredEmployeeIds: Tracks whether an employee ID has been registered to prevent duplicate registrations.

-votes: Records the number of votes each candidate has received.

-totalTokens: A count of total voting tokens issued.

-candidates: An array of candidate names available for voting.

##### 5.Constructor:
Initializes the ERC721 token with a name and symbol.

##### 6.register_voter Function:

-Registers a new voter and mints a new voting token.

-Ensures no duplicate registrations for each employee ID.

##### 7.vote Function:

-Allows token owners to vote for a candidate.

-Requires the caller to be the owner of the token.

##### 8.viewResults Function:

-A view function that returns the current voting results for each candidate.

### Step 2: Deploy the Contract

##### 1.Compile the contract

-Copy the ABI and paste it into a notepad and save this file a a json file.

##### 2. Deploy the VotingSystem contract using the Remix IDE, MetaMask

-Copy the deployed contract address and save it to a .env file.


### Backend Functions Implementation (project_app2.py)

##### Imports and Setup

-Imports: Libraries like os, json, web3, pathlib, dotenv, streamlit, and pandas are imported for various functionalities ranging from blockchain interaction to web app development (import os, import json, etc.).

-Load Environment Variables: load_dotenv() loads environment variables, such as the Web3 provider URI and the smart contract address.

##### Web3 Provider Initialization

-Web3 Provider: Sets up a Web3 provider to interact with the Ethereum blockchain (w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))).

##### Smart Contract Interaction

-Load Contract Function (@st.cache_resource def load_contract()):
  Loads the ABI of the contract from a JSON file.
  Initializes a contract instance using the ABI and contract address.

-Contract Instance: contract = load_contract() gets the contract instance for later use.

##### Employee Dataset

-Load Employee Data: employees = pd.read_csv('fake_employee.csv') loads employee data from a CSV file.

-Data Type Conversion: Converts certain columns from float to int for accurate data handling (employees['employee_id'] = employees['employee_id'].astype(object)).

##### Employee Verification

-Verify Employee Function (def verify_employee(name, phoneNumber, ssnLast4, employeeId)):
  Validates employee information against the dataset.

##### Voter Registration

-Register Voter Function (def register_voter(name, phoneNumber, ssnLast4, employeeId)):
  Checks employee validity.
  Registers a voter on the blockchain using the contract instance.
  Handles any exceptions thrown by the smart contract.

##### Voting Function

-Cast Vote Function (def cast_vote(tokenId, candidate_index)):
  Constructs a transaction to cast a vote on the blockchain.

##### View Results

-View Results Function (def view_results()):
  Fetches and returns the current voting results from the blockchain.

##### Candidate Database

-Candidate Information (candidate_database): Stores detailed information about each candidate, including a bio and image path.

##### Candidate List

-List of Candidates (people): An array of candidate names used in the application.

##### Display Candidates

-Get Candidates Function (def get_candidates()):
  Displays candidate information and images using Streamlit components.



## Frontend Development with Streamlit (Votingapp.py)

The Votingapp.py script is responsible for the frontend of the web application, using Streamlit to create an interactive interface for the voting system. Here's a breakdown of its key components:

### Imports and Initial Setup
-import streamlit as st: Imports Streamlit for building the web application.

-from project_app2 import register_voter, cast_vote, view_results, get_candidates: Imports functions likely for interacting with the blockchain.

-import time: Utilized for handling the voting session timer.

### Streamlit Web Application Structure

##### 1.Website Title (st.title): Sets the title "Company Board Member Voting System" at the top of the page.

##### 2.Timer and Results Viewing (Sidebar):

-Start Timer Button (if st.sidebar.button("Start Timer")): Initiates a 60-minute countdown for the voting session.

-Time Remaining Display (st.sidebar.write): Displays how much time is left in the voting session.

-View Current Results Button (if st.sidebar.button("View Current Results")): When clicked, shows the current vote count for each candidate.

##### 3.Candidate Information Display (get_candidates()):

-Calls a function to possibly fetch and display information about the election candidates.

##### Voter Registration Form

-Form Layout (with st.form("registration_form")): Constructs a form for voter registration.

-Input Fields (st.text_input, st.number_input): Collects user input for name, phone number, SSN's last four digits, and employee ID.

-Registration Logic (if submitted): Executes when the form is submitted, calling register_voter and displaying the outcome.

##### Casting Vote Form

-Form Layout (with st.form("voting_form")): Sets up a form for voters to cast their vote.

-Token ID Field (st.number_input("Token ID")): Input for the voter's token ID.

-Candidate Selector (st.selectbox): Allows voters to choose a candidate from a dropdown.

-Voting Logic (if vote_submitted): Upon form submission, invokes cast_vote and shows a success message or error.

