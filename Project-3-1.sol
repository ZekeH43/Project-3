pragma solidity ^0.8.2;

// SPDX-License-Identifier: UNLICENSED
import "@openzeppelin/contracts/governance/Governor.sol";

abstract contract BoardMemberVotes is Governor("BoardMemberVotes") {
    string private _name;

    mapping(address => Employee) public employees;

    struct Employee {
        string _name;
        string phoneNumber;
        uint256 lastFourSSN;
        uint256 employeeID;
    }

    function registerEmployee(string memory name, string memory phoneNumber, uint256 lastFourSSN, uint256 employeeID) public {
        // Ensure the employee doesn't already exist
        require(employees[msg.sender].employeeID == 0, "Employee already registered");

        // Create a new Employee struct
        Employee memory newEmployee = Employee(
            name = name,
            phoneNumber = phoneNumber,
            lastFourSSN = lastFourSSN,
            employeeID = employeeID
        );

        // Store the employee data
        employees[msg.sender] = newEmployee;
    }

constructor(string memory name) {
        _name = name;
    }

receive() external payable override {
        if (_executor() != address(this)) {
            revert GovernorDisabledDeposit();
        }
    }

    function _countVote(uint256 employeeID, address account) internal virtual {
        return _countVote(employeeID, account);
    }

    function getVotes(address account, uint256 timepoint) override public view returns (uint256) {
        return _getVotes(account, timepoint, _defaultParams());
    }

    function _quorumReached(uint256 proposalId) internal view virtual override returns (bool);

    function _voteSucceeded(uint256 proposalId) internal view virtual override returns (bool);
}