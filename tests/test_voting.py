"""Exercise voting rules and CSV failures without a UI or network connection."""

from dataclasses import astuple

import pytest

from project_app2 import (
    DemoVotingService,
    VotingError,
    load_employees,
    normalize_employee,
    verify_employee,
)


@pytest.fixture
def employees():
    """Load the same small sample dataset used by the app."""
    return load_employees()


def test_registration_and_multiple_candidate_results(employees):
    service = DemoVotingService(employees)
    first = service.register_voter(*astuple(employees[0]))
    second = service.register_voter(*astuple(employees[1]))
    assert (first, second) == (0, 1)
    service.cast_vote(first, 0)
    service.cast_vote(second, 3)
    assert service.view_results() == (1, 0, 0, 1)


def test_verification_preserves_zeroes_and_accepts_name_case_and_phone_format(employees):
    employee = normalize_employee("  demo  EMPLOYEE one ", "(202) 555-0101", "0001", "1001")
    assert employee.ssn_last4 == "0001"
    assert verify_employee(employee, employees)


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", ""),
        ("phone_number", "123"),
        ("ssn_last4", "1"),
        ("employee_id", "0"),
        ("employee_id", "-1"),
        ("employee_id", str(2**256)),
        ("employee_id", "1" * 100),
    ],
)
def test_invalid_employee_fields(field, value):
    values = dict(
        name="Demo Employee One", phone_number="2025550101", ssn_last4="0001", employee_id="1001"
    )
    values[field] = value
    with pytest.raises(VotingError):
        normalize_employee(**values)


def test_mismatched_details_do_not_register_an_employee(employees):
    service = DemoVotingService(employees)
    with pytest.raises(VotingError, match="verification failed"):
        service.register_voter("Demo Employee One", "2025550102", "0001", "1001")
    assert service.register_voter(*astuple(employees[0])) == 0


def test_duplicate_registration_and_vote_are_rejected(employees):
    service = DemoVotingService(employees)
    token = service.register_voter(*astuple(employees[0]))
    with pytest.raises(VotingError, match="already registered"):
        service.register_voter(*astuple(employees[0]))
    service.cast_vote(token, 1)
    snapshot = service.view_results()
    with pytest.raises(VotingError, match="already voted"):
        service.cast_vote(token, 2)
    assert service.view_results() == snapshot == (0, 1, 0, 0)


@pytest.mark.parametrize(
    "token,candidate",
    [(99, 0), (-1, 0), (0, -1), (0, 4), (True, 0), (0, True), (1.2, 0), (2**256, 0)],
)
def test_invalid_ballots_leave_counts_unchanged(employees, token, candidate):
    service = DemoVotingService(employees)
    service.register_voter(*astuple(employees[0]))
    with pytest.raises(VotingError):
        service.cast_vote(token, candidate)
    assert service.view_results() == (0, 0, 0, 0)
    service.cast_vote(0, 0)
    assert service.view_results() == (1, 0, 0, 0)


def test_new_demo_has_independent_state(employees):
    first, second = DemoVotingService(employees), DemoVotingService(employees)
    first.cast_vote(first.register_voter(*astuple(employees[0])), 0)
    assert second.view_results() == (0, 0, 0, 0)


def test_sample_path_is_independent_of_working_directory(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert len(load_employees()) == 4


@pytest.mark.parametrize(
    "contents,message",
    [
        ("name\nDemo\n", "missing required columns"),
        ("employee_id,name,phone_number,Last_4_SSN\n", "at least one record"),
        ("employee_id,name,phone_number,Last_4_SSN\n1,Demo,2025550101,\n", "row 2"),
        (
            "employee_id,name,phone_number,Last_4_SSN\n1,Demo,2025550101,0001\n01,Other,2025550102,0002\n",
            "duplicate employee ID",
        ),
    ],
)
def test_invalid_csv_produces_actionable_error(tmp_path, contents, message):
    path = tmp_path / "employees.csv"
    path.write_text(contents, encoding="utf-8")
    with pytest.raises(VotingError, match=message):
        load_employees(path)


def test_missing_csv_produces_actionable_error(tmp_path):
    with pytest.raises(VotingError, match="Cannot read employee CSV"):
        load_employees(tmp_path / "missing.csv")
