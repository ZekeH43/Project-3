"""Test adapter behavior with simulated receipts; no chain is contacted."""

import json
from dataclasses import astuple
from unittest.mock import MagicMock

import pytest
from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import TimeExhausted

from blockchain import ABI_PATH, ZERO_ADDRESS, BlockchainVotingService, validate_local_provider
from project_app2 import VotingError, load_employees

ACCOUNT = "0x" + "1" * 40
CONTRACT = "0x" + "2" * 40
TX_HASH = HexBytes("0x" + "a" * 64)


@pytest.fixture
def service():
    """Provide a fake node with a confirmed transaction receipt."""
    web3, contract = MagicMock(), MagicMock()
    web3.eth.wait_for_transaction_receipt.return_value = {
        "status": 1,
        "transactionHash": TX_HASH,
    }
    return BlockchainVotingService(web3, contract, ACCOUNT, load_employees())


@pytest.mark.parametrize(
    "uri", ["http://127.0.0.1:8545", "http://localhost:7545", "http://[::1]:8545"]
)
def test_local_providers_are_allowed(uri):
    validate_local_provider(uri)


@pytest.mark.parametrize(
    "uri",
    [
        "https://example.com",
        "http://192.168.1.2:8545",
        "",
        "file:///tmp/node",
        "http://user:password@localhost:8545",
        "http://localhost:99999",
        "http://[broken",
    ],
)
def test_nonlocal_or_invalid_providers_are_rejected(uri):
    with pytest.raises(VotingError, match="local HTTP"):
        validate_local_provider(uri)


def test_success_requires_a_mined_successful_receipt(service):
    assert service.cast_vote(7, 2) == Web3.to_hex(TX_HASH)
    function = service.contract.functions.vote.return_value
    function.transact.assert_called_once_with({"from": ACCOUNT})
    service.web3.eth.wait_for_transaction_receipt.assert_called_once_with(
        function.transact.return_value,
        timeout=120,
    )


def test_reverted_receipt_is_an_error(service):
    service.web3.eth.wait_for_transaction_receipt.return_value["status"] = 0
    with pytest.raises(VotingError, match="reverted"):
        service.cast_vote(0, 0)


def test_timeout_warns_about_pending_transaction_and_does_not_retry(service):
    service.web3.eth.wait_for_transaction_receipt.side_effect = TimeExhausted()
    with pytest.raises(VotingError, match="may still be mined"):
        service.cast_vote(0, 0)
    assert service.contract.functions.vote.return_value.transact.call_count == 1


def test_node_error_is_not_displayed_verbatim(service):
    service.contract.functions.vote.return_value.transact.side_effect = ValueError(
        "private-provider-detail"
    )
    with pytest.raises(VotingError) as caught:
        service.cast_vote(0, 0)
    assert "private-provider-detail" not in str(caught.value)


def test_invalid_details_never_submit_transaction(service):
    with pytest.raises(VotingError, match="verification failed"):
        service.register_voter("Unknown", "2025550101", "0001", "1001")
    service.contract.functions.register_voter.assert_not_called()


def test_invalid_candidate_never_submits_transaction(service):
    with pytest.raises(VotingError):
        service.cast_vote(0, 4)
    service.contract.functions.vote.assert_not_called()


def test_registration_decodes_exact_mint_event_with_real_web3_abi(service):
    """Use real ABI decoding to check the adapter's Web3 v7 event interface."""
    real_contract = Web3().eth.contract(address=CONTRACT, abi=json.loads(ABI_PATH.read_text()))
    service.contract.address = CONTRACT
    service.contract.events = real_contract.events
    receipt = {
        "status": 1,
        "transactionHash": TX_HASH,
        "logs": [
            {
                "address": CONTRACT,
                "topics": [
                    Web3.keccak(text="Transfer(address,address,uint256)"),
                    HexBytes(ZERO_ADDRESS).rjust(32, b"\x00"),
                    HexBytes(ACCOUNT).rjust(32, b"\x00"),
                    HexBytes((42).to_bytes(32, "big")),
                ],
                "data": HexBytes("0x"),
                "logIndex": 0,
                "transactionIndex": 0,
                "transactionHash": TX_HASH,
                "blockHash": TX_HASH,
                "blockNumber": 1,
            }
        ],
    }
    service.web3.eth.wait_for_transaction_receipt.return_value = receipt
    assert service.register_voter(*astuple(load_employees()[0])) == 42
    service.contract.functions.totalTokens.assert_not_called()


def test_missing_mint_event_does_not_invent_a_token_id(service):
    service.contract.events.Transfer.return_value.process_receipt.return_value = []
    with pytest.raises(VotingError, match="Registration confirmed"):
        service.register_voter(*astuple(load_employees()[0]))


def test_results_are_read_without_a_transaction(service):
    service.contract.functions.viewResults.return_value.call.return_value = [2, 0, 1, 4]
    assert service.view_results() == (2, 0, 1, 4)
    service.contract.functions.viewResults.return_value.transact.assert_not_called()
