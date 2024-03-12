##Tech Company Board Member Voting System
#Overview
-We are creating a voting system for a tech company to cast votes on who they want to be added as a board member. This system is designed to ensure a transparent and secure voting process using blockchain technology and a user-friendly interface.

##Solidity Contract Implementation (Project_33.sol)
-The smart contract, written in Solidity, facilitates a secure and transparent voting process for board member selection. Key components include:

-ERC721 Token: Inherits from ERC721Full, an OpenZeppelin implementation of the ERC721 standard, creating unique tokens for each voter.
-Voter Structure: A Voter struct stores information such as name, phone number, last four digits of SSN, and employee ID.
-Mappings:
--voters: Maps token IDs to Voter objects.
--registeredEmployeeIds: Tracks registered employee IDs to prevent duplicate registrations.
---votes: Maps candidate indices to their vote counts.
-Candidates: An array of candidate names for the election.
--register_voter Function: Registers voters and mints new ERC721 tokens, ensuring no duplicate registrations.
--vote Function: Allows token owners to vote for candidates.
--viewResults Function: A public view function that returns the total votes each candidate has received.
-Contract Compilation and ABI Generation
-After completing the Solidity contract, we compiled it and extracted the ABI (Application Binary Interface). The ABI was saved as a JSON file for interaction with the contract from our Python application.

MetaMask Integration and Contract Deployment
We connected our project to MetaMask and deployed the contract to the Ethereum network. The contract address and Web3 provider URI were stored in an .env file for secure interactions.

Data Preparation
A dataset of fake employee information from Kaggle (fake_employee.csv) was used to validate employee registration in the Python application.

Backend Functions Implementation (project_app2.py)
The backend functions in project_app2.py interact with the blockchain smart contract and perform operations like:

Contract Interaction Setup: Connects with the Ethereum blockchain and sets up the contract instance.
Voter Registration Function: Registers voters in the system, handling responses from the smart contract.
Voting Function: Allows users to vote for candidates and sends transactions to the smart contract.
Results Viewing Function: Fetches and displays voting results.
Employee Verification: Validates voter registration using the fake employee dataset.
Frontend Development with Streamlit (Votingapp.py)
The Streamlit frontend application offers:

Website Title: "Company Board Member Voting System."
Sidebar for Timer and Results Viewing: Includes a voting session timer and a button to view current voting results.
Candidate Information Display: Functionality to show candidate details.
Voter Registration Form: A form for voter registration, interacting with the register_voter function.
Casting Vote Form: Allows registered voters to cast their votes and displays the outcome.
This Streamlit application provides a convenient interface for employees to participate in the voting process, from registration to casting votes and viewing results.
