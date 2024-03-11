pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract VotingSystem is ERC721Full {
    struct  Voter {
        string name;
        string phoneNumber;
        uint ssnLast4;
        uint employeeId;
    }

    mapping(uint => Voter) public voters;
    mapping(uint => uint) public votes;
    uint public totalTokens;
    string[4] public candidates = ["Alice", "Bob", "Charlie", "Diana"];

    constructor() ERC721Full ("VotingToken", "VOTE") public {}

    function registerVoter(string memory _name, string memory _phoneNumber, uint _ssnLast4, uint _employeeId) public {
        uint tokenId = totalTokens++;
        voters[tokenId] = Voter(_name, _phoneNumber, _ssnLast4, _employeeId);
        _mint(msg.sender, tokenId);
    }

    function vote(uint _tokenId, uint _candidateIndex) public {
        require(ownerOf(_tokenId) == msg.sender, "Not the token owner");
        votes[_candidateIndex]++;
    }

    function viewResults() public view returns (uint[4] memory) {
        uint[4] memory results;
        for (uint i = 0; i < candidates.length; i++) {
            results[i] = votes[i];
        }
        return results;
    }
}
