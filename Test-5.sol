// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;
// Import the ERC20 interface
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
contract BoardMemberElection {
    // Structure to represent a candidate
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }
    // Structure to represent an employee (voter)
    struct Employee {
        string name;
        string phoneNumber;
        uint256 lastFourSSN;
        uint256 employeeID;
        bool voted;
        uint voteIndex;
        uint tokens;
    }
    // Address of the owner who deploys the contract
    address public owner;
    // Mapping of addresses to employees (voters)
    mapping(address => Employee) public employees;
    // Mapping of employee ID to address to check for duplicate registrations
    mapping(uint256 => address) public employeeIDToAddress;
    // Array of candidates
    Candidate[] public candidates;
    // Address of the token contract
    address public tokenAddress;
    // Modifier to restrict function access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }
    // Constructor to initialize contract with two candidates
    constructor(address _tokenAddress) {
        owner = msg.sender;
        tokenAddress = _tokenAddress;
        addCandidate("Candidate 1");
        addCandidate("Candidate 2");
    }
    // Function to add candidates (only callable by the owner)
    function addCandidate(string memory _name) public onlyOwner {
        require(candidates.length < 2, "Maximum number of candidates reached");
        uint candidateId = candidates.length;
        candidates.push(Candidate(candidateId, _name, 0));
    }
    // Function to allow employees (voters) to register for voting
    function registerEmployee(string memory _name, string memory _phoneNumber, uint256 _lastFourSSN, uint256 _employeeID) public {
        // Ensure the employee ID is not already registered
        require(employeeIDToAddress[_employeeID] == address(0), "Employee ID already registered");
        // Ensure the employee doesn't already exist
        require(employees[msg.sender].employeeID == 0, "Employee already registered");
        // Create a new Employee struct
        Employee memory newEmployee = Employee(
            _name,
            _phoneNumber,
            _lastFourSSN,
            _employeeID,
            false,
            0,
            0
        );
        // Store the employee data
        employees[msg.sender] = newEmployee;
        // Update the mapping of employee ID to address
        employeeIDToAddress[_employeeID] = msg.sender;
    }
    // Function to allow employees (voters) to cast their vote using tokens
    function vote(uint _candidateId, uint _tokens) public {
        require(!employees[msg.sender].voted, "You have already voted");
        require(_candidateId < candidates.length, "Invalid candidate ID");
        // Transfer tokens from the employee to the contract
        IERC20 token = IERC20(tokenAddress);
        token.transferFrom(msg.sender, address(this), _tokens);
        employees[msg.sender].voted = true;
        employees[msg.sender].voteIndex = _candidateId;
        employees[msg.sender].tokens = _tokens;
        candidates[_candidateId].voteCount += _tokens;
    }
    // Function to get the winner
    function getWinner() public view returns (string memory) {
        uint maxVoteCount = 0;
        uint winningCandidateId;
        for (uint i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > maxVoteCount) {
                maxVoteCount = candidates[i].voteCount;
                winningCandidateId = i;
            }
        }
        return candidates[winningCandidateId].name;
    }
}