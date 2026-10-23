# Board Member Voting Demo

A Python and Streamlit application that lets a reviewer register fictional
employees, issue voting tokens, cast ballots, and inspect candidate totals.
The default **offline demo runs without a wallet, blockchain node, or API key**.
An optional adapter preserves the original Solidity integration for a local
learning environment.

**Project status:** educational portfolio prototype. The offline demo is tested;
the legacy smart contract is not suitable for a real election.

## What the project demonstrates

- Python functions, dataclasses, dictionaries, sets, and input validation.
- CSV loading with explicit schema checks and preservation of leading zeroes.
- A Streamlit interface separated from voting rules and blockchain calls.
- Error handling that distinguishes a rejected request from a successful action.
- Automated tests of business rules, Streamlit forms, and transaction receipts.
- An optional Web3 adapter that waits for confirmation and reads minted token IDs
  from transaction events rather than guessing from a global counter.

## Quick start

Use **Python 3.11 or 3.12** and Git. Clone the repository and enter its folder:

```bash
git clone https://github.com/ZekeH43/Project-3.git
cd Project-3
```

### Windows PowerShell

These commands use the environment's Python directly; activating a script is
not required.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run Votingapp.py
```

Use `py -3.11` in the first command if Python 3.11 is installed instead.

### Linux, WSL, or macOS

Check `python3 --version` first, then run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run Votingapp.py
```

Open the local URL printed in the terminal, normally `http://localhost:8501`.
Keep **Demo (no blockchain)** selected. No `.env` file is needed.

## Try it in two minutes

1. Expand **Sample employees** in the app.
2. Register this fictional employee:

   | Field | Value |
   | --- | --- |
   | Name | Demo Employee One |
   | Phone number | 2025550101 |
   | Demo SSN suffix | 0001 |
   | Employee ID | 1001 |

3. The first successful registration returns **token ID 0**.
4. Enter token `0`, select **Alice**, and click **Vote**. Results become
   Alice: 1, Bob: 0, Charlie: 0, Diana: 0.
5. Try voting with token `0` again. The demo rejects the repeat vote and leaves
   counts unchanged.
6. Click **Reset demo** to start over, or register another sample employee.

All four sample records are deliberately fictional. Do not enter real SSNs,
private keys, or real employee information.

## How it works

`Votingapp.py` collects input and calls a service. `project_app2.py` normalizes
and verifies details against `examples/employees.csv`, then manages the demo's
registrations and votes. `blockchain.py` implements the corresponding operations
against the original contract when local blockchain mode is selected.

A successful registration returns an integer token ID. Failures raise
`VotingError`, which the interface displays as an error. Success messages occur
only in the successful branch of that operation.

| File or folder | Purpose |
| --- | --- |
| `Votingapp.py` | Streamlit entry point, forms, and results |
| `project_app2.py` | Data models, CSV validation, and offline voting rules |
| `blockchain.py` | Optional local-chain configuration and transaction handling |
| `examples/employees.csv` | Four fictional records used by both modes |
| `Images/` | Original candidate images |
| `tests/` | Domain, interface, and Web3 adapter tests |
| `docs/WALKTHROUGH.md` | Code-reading guide and interview practice |
| `docs/BLOCKCHAIN.md` | Optional deployment instructions and contract limitations |
| `Project_33 (2).sol` | Original Solidity 0.5 contract, retained for study |
| `contracts/compiled/project_3.json` | Original ABI; this is not deployment bytecode |
| `fake_employee.csv` | Original class dataset, retained as historical material |
| `Project 3.pptx`, `Project Proposal*.docx` | Original project deliverables |

The original CSV is not loaded by the app. It contains duplicate employee ID
`7829`, which is incompatible with unique employee registration. The new small
fixture is explicit, deterministic, and easy to demonstrate.

## Tests and code checks

Install the development requirements using the same virtual environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

Here `python` means `.venv/bin/python` on Linux/WSL/macOS or
`.\.venv\Scripts\python.exe` on Windows, unless the environment is activated.
The development requirements also install optional blockchain dependencies so
the adapter tests can run. No tests send transactions or require a live node.

Tests cover invalid input, duplicate registrations and votes, CSV errors,
independent demo sessions, actual Streamlit form interactions, failed receipts,
confirmation timeouts, and decoding a synthetic mint event with the real Web3 ABI.
GitHub Actions runs the checks on Python 3.11 and 3.12.

## Optional blockchain mode

Follow [the local blockchain guide](docs/BLOCKCHAIN.md). This mode requires an
additional dependency file, a local development node, the deployed original
contract, and a local `.env` copied from `.env.example`.

The Python adapter checks transaction receipts. It does **not** fix the legacy
contract's missing voting restrictions. Blockchain deployment and end-to-end
transactions require separate local validation; the automated suite uses
simulated receipts.

## Limitations and next steps

- Demo state belongs to one browser session and is lost on reset, session loss,
  or server restart. Different browsers do not share an election.
- Sample-data verification and token IDs are not authentication. The demo is a
  walkthrough, not an election service.
- The original contract permits repeat votes, lacks candidate bounds checks,
  stores registration details publicly, and does not enforce election deadlines.
- The original screen-only timer was removed because it did not enforce a voting
  deadline. A real deadline must be enforced by the system recording votes.
- `.env` and notebook/cache artifacts are no longer tracked in this revision.
  Earlier commits still contain a private key. Any non-disposable use requires
  key replacement; deleting a file does not remove its history.

Useful next increments are SQLite persistence for the Python demo, a real
identity/authorization design, and a separately tested replacement contract that
stores no personal information and enforces one vote and an election deadline.

## Project history

This repository retains the original project assets and Solidity prototype.
The cleanup adds a runnable demo, separates responsibilities, fixes Python
failure handling, and documents what remains incomplete. Existing Git history
preserves original contributions; this README does not claim sole authorship of
team materials or results that have not been measured.

For a guided explanation of the implementation, read
[the walkthrough](docs/WALKTHROUGH.md).
