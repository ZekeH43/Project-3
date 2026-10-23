# Original blockchain integration: local development only

The default Python demo is the easiest way to review this project. This optional
mode preserves the original Solidity API for learning. It is **not** a secure
election system and must only use disposable test accounts and fictional data.

## What is included

- `Project_33 (2).sol`: the original `VotingSystem` contract, using Solidity
  `^0.5.5` and the OpenZeppelin `release-v2.5.0` ERC721 implementation.
- `contracts/compiled/project_3.json`: the original ABI, not bytecode.
- `blockchain.py`: a Web3 7 adapter using an unlocked account on a local node.

The contract source and ABI were retained. This Python cleanup does not deploy
or modify a contract, move funds, or establish that an old deployment still runs.

## Setup

1. Install the optional dependencies in the virtual environment:

   ```bash
   python -m pip install -r requirements-blockchain.txt
   ```

2. Start a disposable Ethereum-compatible development node that exposes HTTP RPC
   on loopback and provides unlocked, funded **test** accounts. Use its actual
   port; the example configuration uses `127.0.0.1:8545`.
3. Open the Solidity source in [Remix](https://remix.ethereum.org/). Select a
   compiler compatible with `^0.5.5`, such as `0.5.17`, and compile the contract.
   The historical OpenZeppelin import requires internet access.
4. Deploy `VotingSystem` to that same local node using an unlocked test account.
   Choose an environment connected to your local RPC endpoint. Remix's
   browser-only VM is not automatically reachable by the Python HTTP client.
5. Copy `.env.example` to `.env`:

   ```powershell
   # Windows PowerShell
   Copy-Item .env.example .env
   ```

   ```bash
   # Linux, WSL, or macOS
   cp .env.example .env
   ```

6. Set `WEB3_PROVIDER_URI` to the local RPC endpoint and
   `SMART_CONTRACT_ADDRESS` to the address returned by deployment. Optionally
   set `WEB3_ACCOUNT_ADDRESS` to an unlocked test account exposed by that node.
   Otherwise the app uses the node's first account. **Do not add a private key.**
7. Start `python -m streamlit run Votingapp.py`, choose **Local blockchain
   (legacy)**, and register a fictional employee from the sample table.

Use the virtual environment's Python executable for these commands, as shown in
the main README. Keep the app and node in the same environment when possible;
`localhost` inside WSL or a container may differ from the host's `localhost`.
After configuration changes, restart Streamlit so environment variables loaded
from the previous `.env` do not take precedence. **Reconnect local node** rebuilds
the client for the current process configuration.

The adapter rejects remote RPC URLs, missing addresses, absent deployed code,
unavailable node accounts, and a different candidate order. Loopback validation
prevents accidental use of a remote URL; it is not a security sandbox for a
forwarding proxy or a compromised local node.

## Transaction behavior

Registration verifies the sample data, submits the transaction, waits for its
receipt, checks `status == 1`, and decodes the minted token from the receipt's
ERC721 `Transfer` event. Voting similarly waits for a successful receipt.
Results use a read-only contract call.

If confirmation times out or the connection fails after submission, the
transaction might still be mined. Inspect the local node before retrying.
The app does not automatically resend it. If registration confirms but the mint
event cannot be decoded, inspect that receipt instead of registering again.

## Known contract limitations

| Finding in the original source | Consequence | Required redesign |
| --- | --- | --- |
| `vote` never records whether a token voted | One token can vote repeatedly | Enforce one vote per eligible voter on-chain |
| No candidate bounds check | Direct callers can increment unused candidate indices | Validate the index in the contract |
| Public registration accepts arbitrary employee IDs | Python CSV checks can be bypassed by direct calls | Establish trusted authorization before minting |
| Name, phone, and SSN suffix are stored publicly | Registration data is visible on-chain | Keep personal information off-chain |
| ERC721 tokens are transferable | Eligibility can be transferred to another account | Define non-transferable voting eligibility |
| One unlocked account sends all UI transactions | The app does not authenticate separate voters | Design per-voter identity and authorization |
| No enforced election deadline | A UI timer cannot close voting | Enforce a deadline in the recording system |

The offline demo rejects duplicate votes within its own session. That behavior
must not be mistaken for a fix to the original contract.

## Verification and credential history

Automated tests simulate RPC responses and receipts, and decode a synthetic
`Transfer` event through the real Web3 ABI. They do not compile or deploy the
Solidity contract or test a live node. A contract replacement needs its own
deployment procedure, adversarial tests, and review.

An earlier tracked `.env` contains a private key. The cleanup removes tracked
environment files and adds ignore rules, but old commits remain. If that key was
used beyond a disposable development chain, treat it as exposed and replace it.
Do not reuse it in this app. History rewriting, if needed, is a separate
coordinated operation because it affects existing clones and branches.

## References

- [Web3 7 contract API](https://web3py.readthedocs.io/en/v7.14.1/web3.contract.html)
- [Web3 transaction receipts](https://web3py.readthedocs.io/en/v7.14.1/web3.eth.html)
- [Streamlit app testing](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)
