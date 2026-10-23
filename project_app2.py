"""Employee validation and an offline voting demo, independent of Streamlit.

Start the interface with ``python -m streamlit run Votingapp.py``. The demo
keeps its state in one browser session; it is not an authentication system.
"""

import csv
import re
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
EMPLOYEE_FILE = PROJECT_ROOT / "examples" / "employees.csv"
UINT256_MAX = 2**256 - 1


class VotingError(ValueError):
    """An input or voting error that can be displayed to the user."""


@dataclass(frozen=True)
class Employee:
    """Synthetic employee details; strings preserve leading zeroes."""

    name: str
    phone_number: str
    ssn_last4: str
    employee_id: str


@dataclass(frozen=True)
class Candidate:
    """Candidate information shared by the ballot and results display."""

    name: str
    bio: str
    image: Path


CANDIDATES = (
    Candidate("Alice", "Chip designer and outdoor enthusiast.", PROJECT_ROOT / "Images/Alice.jpg"),
    Candidate(
        "Bob",
        "Chip manufacturing specialist and enthusiastic cook.",
        PROJECT_ROOT / "Images/Bob.jpg",
    ),
    Candidate(
        "Charlie",
        "Chip designer, musician, and guitar player.",
        PROJECT_ROOT / "Images/Charlie.jpg",
    ),
    Candidate("Diana", "Chip engineer and avid reader.", PROJECT_ROOT / "Images/Diana.jpg"),
)


def normalize_employee(name: str, phone_number: str, ssn_last4: str, employee_id: str) -> Employee:
    """Validate form input and normalize spaces and phone punctuation.

    SSN suffixes and IDs are text, not measurements. Keeping them as strings
    avoids losing zeroes before verification against a CSV record.
    """
    name = " ".join(name.split())
    phone_number = re.sub(r"[\s().-]", "", phone_number)
    ssn_last4 = ssn_last4.strip()
    employee_id = employee_id.strip()
    if not name:
        raise VotingError("Enter a name from the sample employee list.")
    if not re.fullmatch(r"[0-9]{10}", phone_number):
        raise VotingError("Phone number must contain 10 digits.")
    if not re.fullmatch(r"[0-9]{4}", ssn_last4):
        raise VotingError("Demo SSN suffix must contain exactly 4 digits.")
    if not re.fullmatch(r"[0-9]{1,78}", employee_id):
        raise VotingError("Employee ID must contain only digits (up to 78).")
    if not 0 < int(employee_id) <= UINT256_MAX:
        raise VotingError("Employee ID must be a positive uint256 value.")
    return Employee(name, phone_number, ssn_last4, employee_id)


def load_employees(path: Path = EMPLOYEE_FILE) -> tuple[Employee, ...]:
    """Read a sample CSV without depending on the working directory.

    Missing columns, malformed records, and duplicate IDs are reported before
    registration. CSV fields remain strings so leading zeroes are preserved.
    """
    required = {"name", "phone_number", "Last_4_SSN", "employee_id"}
    employees = []
    seen_ids = set()
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            if not required.issubset(reader.fieldnames or []):
                raise VotingError("Employee CSV is missing required columns.")
            for line_number, row in enumerate(reader, start=2):
                try:
                    employee = normalize_employee(
                        row["name"] or "",
                        row["phone_number"] or "",
                        row["Last_4_SSN"] or "",
                        row["employee_id"] or "",
                    )
                except VotingError as error:
                    raise VotingError(f"Employee CSV row {line_number}: {error}") from error
                # Solidity treats 01001 and 1001 as the same numeric ID.
                numeric_id = int(employee.employee_id)
                if numeric_id in seen_ids:
                    raise VotingError(f"Employee CSV row {line_number}: duplicate employee ID.")
                seen_ids.add(numeric_id)
                employees.append(employee)
    except (OSError, UnicodeError, csv.Error) as error:
        raise VotingError("Cannot read employee CSV. Check the file path and encoding.") from error
    if not employees:
        raise VotingError("Employee CSV must contain at least one record.")
    return tuple(employees)


def verify_employee(employee: Employee, employees: tuple[Employee, ...]) -> bool:
    """Match all fields to one row; demo validation is not real identity proof."""
    return any(
        employee.name.casefold() == record.name.casefold()
        and employee.phone_number == record.phone_number
        and employee.ssn_last4 == record.ssn_last4
        and employee.employee_id == record.employee_id
        for record in employees
    )


def validate_vote(token_id: int, candidate_index: int) -> None:
    """Reject invalid IDs and candidate indices before changing state."""
    if type(token_id) is not int or not 0 <= token_id <= UINT256_MAX:
        raise VotingError("Token ID must be a non-negative uint256 integer.")
    if type(candidate_index) is not int or not 0 <= candidate_index < len(CANDIDATES):
        raise VotingError("Choose one of the listed candidates.")


class DemoVotingService:
    """An in-memory election used by one Streamlit browser session.

    Registration returns a token ID. Each registered token can cast one vote.
    A new service starts a new election; there is no disk or blockchain storage.
    """

    def __init__(self, employees: tuple[Employee, ...]) -> None:
        self.employees = employees
        self._registered_ids: set[str] = set()
        self._voters: dict[int, Employee] = {}
        self._voted_tokens: set[int] = set()
        self._votes = [0] * len(CANDIDATES)

    def register_voter(self, name: str, phone_number: str, ssn_last4: str, employee_id: str) -> int:
        """Verify sample details and return a unique, zero-based token ID."""
        employee = normalize_employee(name, phone_number, ssn_last4, employee_id)
        if not verify_employee(employee, self.employees):
            raise VotingError("Employee verification failed. Use a matching sample record.")
        if employee.employee_id in self._registered_ids:
            raise VotingError("This employee is already registered in this demo session.")
        token_id = len(self._voters)
        self._voters[token_id] = employee
        self._registered_ids.add(employee.employee_id)
        return token_id

    def cast_vote(self, token_id: int, candidate_index: int) -> None:
        """Record one vote, leaving counts unchanged when validation fails."""
        validate_vote(token_id, candidate_index)
        if token_id not in self._voters:
            raise VotingError("Register first and use the token ID you receive.")
        if token_id in self._voted_tokens:
            raise VotingError("This token has already voted in this demo session.")
        self._votes[candidate_index] += 1
        self._voted_tokens.add(token_id)

    def view_results(self) -> tuple[int, ...]:
        """Return a snapshot so callers cannot change the internal counts."""
        return tuple(self._votes)
