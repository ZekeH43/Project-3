pragma solidity ^0.8.2;
// SPDX-License-Identifier: UNLICENSED
import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

contract BoardMemberVotes is Governor, GovernorCountingSimple, GovernorSettings, GovernorVotes, GovernorVotesQuorumFraction, GovernorTimelockControl
{

    function _cancel(uint256 proposalId) internal override {
    // Your implementation for the _cancel function goes here
    }
    struct Employee {
        string name;
        string phoneNumber;
        uint256 lastFourSSN;
        uint256 employeeID;
    }
    mapping(address => Employee) public employees;
    
    function registerEmployee(string memory _name, string memory _phoneNumber, uint256 _lastFourSSN, uint256 _employeeID) public {
        // Ensure the employee doesn't already exist
        require(employees[msg.sender].employeeID == 0, "Employee already registered");
        
        // Create a new Employee struct
        Employee memory newEmployee = Employee({
            name: _name,
            phoneNumber: _phoneNumber,
            lastFourSSN: _lastFourSSN,
            employeeID: _employeeID
        });
        
        // Store the employee data
        employees[msg.sender] = newEmployee;
    }
}


