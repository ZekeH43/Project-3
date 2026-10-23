"""Optional adapter for the original Solidity contract on a local test chain.

The legacy contract is not suitable for a real election. See
``docs/BLOCKCHAIN.md`` for setup, limitations, and the required redesign.
No connection or transaction is made merely by importing this module.
"""

import ipaddress
import json
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from requests.exceptions import RequestException
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import TimeExhausted, Web3Exception
from web3.logs import DISCARD

from project_app2 import (
    CANDIDATES,
    PROJECT_ROOT,
    Employee,
    VotingError,
    normalize_employee,
    validate_vote,
    verify_employee,
)

ZERO_ADDRESS = "0x" + "0" * 40
ABI_PATH = PROJECT_ROOT / "contracts" / "compiled" / "project_3.json"
RPC_ERRORS = (Web3Exception, RequestException, ValueError)


def validate_local_provider(uri: str) -> None:
    """Allow HTTP(S) loopback endpoints only; never connect this demo to mainnet."""
    try:
        parsed = urlparse(uri)
        host = parsed.hostname
        # Accessing port also validates malformed/out-of-range port numbers.
        _ = parsed.port
        local = host == "localhost" or (host is not None and ipaddress.ip_address(host).is_loopback)
    except ValueError:
        local = False
    if not local or parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        raise VotingError("WEB3_PROVIDER_URI must be a local HTTP(S) loopback endpoint.")


class BlockchainVotingService:
    """Send transactions from one explicitly selected unlocked local test account.

    This adapter preserves the original contract API. It cannot repair missing
    authorization or one-vote enforcement in an already-deployed contract.
    """

    def __init__(
        self, web3: Web3, contract: Contract, account: str, employees: tuple[Employee, ...]
    ) -> None:
        self.web3 = web3
        self.contract = contract
        self.account = account
        self.employees = employees

    def _submit(self, function):
        """Wait for mining and check receipt status before reporting success.

        Let the local node choose the nonce. A timeout does not mean the
        transaction failed, so callers must not automatically resubmit it.
        """
        try:
            transaction_hash = function.transact({"from": self.account})
            receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=120)
        except TimeExhausted as error:
            raise VotingError(
                "Confirmation timed out. Check the local chain before retrying; "
                "the transaction may still be mined."
            ) from error
        except RPC_ERRORS as error:
            raise VotingError(
                "Could not confirm the transaction. Check the local chain and account "
                "before retrying."
            ) from error
        if receipt.get("status") != 1:
            raise VotingError("The transaction was mined but reverted; no change was recorded.")
        return receipt

    def register_voter(self, name: str, phone_number: str, ssn_last4: str, employee_id: str) -> int:
        """Verify sample details and read the minted token ID from this receipt.

        Reading totalTokens - 1 is unsafe because another registration could
        be mined first. The Transfer event belongs to this exact transaction.
        """
        employee = normalize_employee(name, phone_number, ssn_last4, employee_id)
        if not verify_employee(employee, self.employees):
            raise VotingError("Employee verification failed. Use a matching sample record.")
        receipt = self._submit(
            self.contract.functions.register_voter(
                employee.name,
                int(employee.phone_number),
                int(employee.ssn_last4),
                int(employee.employee_id),
            )
        )
        try:
            events = self.contract.events.Transfer().process_receipt(receipt, errors=DISCARD)
            tokens = [
                event["args"]["tokenId"]
                for event in events
                if event["address"].lower() == self.contract.address.lower()
                and event["args"]["from"].lower() == ZERO_ADDRESS
                and event["args"]["to"].lower() == self.account.lower()
            ]
        except (Web3Exception, KeyError, TypeError, ValueError) as error:
            raise VotingError(
                "Registration confirmed, but the token event could not be decoded. "
                "Inspect the receipt before trying again."
            ) from error
        if len(tokens) != 1:
            raise VotingError(
                "Registration confirmed, but no unique minted token was found. "
                "Check the contract ABI and receipt before trying again."
            )
        return int(tokens[0])

    def cast_vote(self, token_id: int, candidate_index: int) -> str:
        """Validate input, wait for confirmation, and return the transaction hash."""
        validate_vote(token_id, candidate_index)
        receipt = self._submit(self.contract.functions.vote(token_id, candidate_index))
        return Web3.to_hex(receipt["transactionHash"])

    def view_results(self) -> tuple[int, ...]:
        """Read candidate counts without sending a transaction."""
        try:
            results = self.contract.functions.viewResults().call()
        except RPC_ERRORS as error:
            raise VotingError(
                "Cannot read results. Check the local node, contract address, and ABI."
            ) from error
        if len(results) != len(CANDIDATES) or any(type(n) is not int or n < 0 for n in results):
            raise VotingError("Contract results do not match the expected candidate list.")
        return tuple(results)


def create_blockchain_service(employees: tuple[Employee, ...]) -> BlockchainVotingService:
    """Load local configuration and verify the node, account, and deployed code."""
    load_dotenv(PROJECT_ROOT / ".env", override=False)
    uri = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
    validate_local_provider(uri)
    address = os.getenv("SMART_CONTRACT_ADDRESS", "").strip()
    if not Web3.is_address(address):
        raise VotingError("Set SMART_CONTRACT_ADDRESS in .env to your local deployment address.")
    try:
        with ABI_PATH.open(encoding="utf-8") as source:
            abi = json.load(source)
    except (OSError, ValueError) as error:
        raise VotingError("Cannot load contracts/compiled/project_3.json.") from error
    if not isinstance(abi, list):
        raise VotingError("The contract ABI must be a JSON array.")
    web3 = Web3(Web3.HTTPProvider(uri, request_kwargs={"timeout": 10}))
    try:
        if not web3.is_connected():
            raise VotingError("Cannot connect to the local development node.")
        accounts = web3.eth.accounts
        selected = os.getenv("WEB3_ACCOUNT_ADDRESS", "").strip()
        if not selected and not accounts:
            raise VotingError("The local node has no unlocked test accounts.")
        account = Web3.to_checksum_address(selected or accounts[0])
        if account not in [Web3.to_checksum_address(item) for item in accounts]:
            raise VotingError("WEB3_ACCOUNT_ADDRESS must be an unlocked account on the local node.")
        address = Web3.to_checksum_address(address)
        if not web3.eth.get_code(address):
            raise VotingError("No contract is deployed at SMART_CONTRACT_ADDRESS on this node.")
        contract = web3.eth.contract(address=address, abi=abi)
        names = tuple(contract.functions.candidates(i).call() for i in range(len(CANDIDATES)))
        if names != tuple(candidate.name for candidate in CANDIDATES):
            raise VotingError("The deployed contract uses a different candidate list.")
    except VotingError:
        raise
    except RPC_ERRORS as error:
        raise VotingError(
            "Local blockchain setup failed. Check the node, account, address, and ABI."
        ) from error
    return BlockchainVotingService(web3, contract, account, employees)
