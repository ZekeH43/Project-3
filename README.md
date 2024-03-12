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











































































































# Tech Company Board Member Voting System


## Overview

-We are creating a voting system for a tech company to cast votes on who they want to be added as a board member. This system is designed to ensure a transparent and secure voting process using blockchain technology and a user-friendly interface.


## Solidity Contract Implementation (Project_33.sol)

The smart contract, written in Solidity, facilitates a secure and transparent voting process for board member selection. Key components include:

  -ERC721 Token: Inherits from ERC721Full, an OpenZeppelin implementation of the ERC721 standard, creating unique tokens for each voter.

  -Voter Structure: A Voter struct stores information such as name, phone number, last four digits of SSN, and employee ID.

  -Mappings:
    voters: Maps token IDs to Voter objects.
    registeredEmployeeIds: Tracks registered employee IDs to prevent duplicate registrations.
    votes: Maps candidate indices to their vote counts.
    
  -Candidates: An array of candidate names for the election.
  
  -register_voter Function: Registers voters and mints new ERC721 tokens, It check sif the employeeID is already registered using 'registeredEmployeedIds' ensuring no duplicate registrations.
  
  -vote Function: Allows token owners to vote for candidates.
  
  -viewResults Function: A public view function that returns the total votes each candidate has received.

  
## Contract Compilation and ABI Generation

After completing the Solidity contract, we compiled it and extracted the ABI (Application Binary Interface). The ABI was saved as a JSON file for interaction with the contract from our Python application.

## MetaMask Integration and Contract Deployment

We connected our project to MetaMask and deployed the contract to the Ethereum network. The contract address and Web3 provider URI were stored in an .env file for secure interactions.

## Data Preparation

A dataset of fake employee information from Kaggle (fake_employee.csv) was used to validate employee registration in the Python application.

## Backend Functions Implementation (project_app2.py)

The backend functions in project_app2.py interact with the blockchain smart contract and perform operations like:

  -Contract Interaction Setup: Connects with the Ethereum blockchain and sets up the contract instance.
  
-Voter Registration Function: Registers voters in the system, handling responses from the smart contract.

  -Voting Function: Allows users to vote for candidates and sends transactions to the smart contract.
  
  -Results Viewing Function: Fetches and displays voting results.
  
  -Employee Verification: Validates voter registration using the fake employee dataset.


## Frontend Development with Streamlit (Votingapp.py)

The frontend of our voting system is an interactive web application developed using Streamlit. It provides a user-friendly interface for participating in the board member voting process. Key features of the application include:

  -Website Title: Displays the title "Company Board Member Voting System" at the top of the page.

  -Sidebar for Timer and Results Viewing:
    Start Timer: A button to start a voting session timer, lasting for one hour. It displays the remaining time in the sidebar.
    View Current Results: A button to view the current voting results. When clicked, it displays the vote count for each candidate.
    
  -Candidate Information Display: Functionality to retrieve and show information about the candidates. (The specific implementation details of get_candidates() are not provided, but it presumably fetches and displays candidate details.)

  -Voter Registration Form:
    A form where users can input their name, phone number, last four digits of SSN, and employee ID for voter registration.
    On submission, it calls the register_voter function from project_app2.py and displays the registration status.
    
  -Casting Vote Form:
    A form for registered voters to cast their vote. Voters enter their token ID and select a candidate from a dropdown list.
    On submission, it calls the cast_vote function from project_app2.py and displays a success or error message based on the voting outcome.
