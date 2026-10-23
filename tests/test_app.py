"""Run the actual Streamlit forms to catch misleading success messages."""

from streamlit.testing.v1 import AppTest

from project_app2 import PROJECT_ROOT


def fill_registration(app, name="Demo Employee One"):
    """Fill the four registration fields with one synthetic record."""
    for key, value in {
        "employee_name": name,
        "employee_phone": "2025550101",
        "employee_suffix": "0001",
        "employee_id": "1001",
    }.items():
        app.text_input(key).set_value(value)


def test_demo_registration_voting_repeat_vote_and_reset():
    app = AppTest.from_file(str(PROJECT_ROOT / "Votingapp.py")).run()
    assert not app.exception
    fill_registration(app)
    app.button("register").click().run()
    assert not app.exception
    assert "token ID is 0" in app.success[0].value
    app.button("vote").click().run()
    assert not app.exception
    assert app.success[0].value == "Vote recorded successfully."
    assert app.table[-1].value["Votes"].tolist() == [1, 0, 0, 0]
    app.button("vote").click().run()
    assert "already voted" in app.error[0].value
    assert not app.success
    assert app.table[-1].value["Votes"].tolist() == [1, 0, 0, 0]
    app.button("reset_demo").click().run()
    assert not app.exception
    assert app.table[-1].value["Votes"].tolist() == [0, 0, 0, 0]


def test_failed_registration_never_displays_success():
    app = AppTest.from_file(str(PROJECT_ROOT / "Votingapp.py")).run()
    fill_registration(app, name="Unrecognized Employee")
    app.button("register").click().run()
    assert not app.exception
    assert "verification failed" in app.error[0].value
    assert not app.success


def test_missing_blockchain_configuration_has_helpful_error(monkeypatch):
    monkeypatch.setenv("SMART_CONTRACT_ADDRESS", "")
    monkeypatch.setenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
    app = AppTest.from_file(str(PROJECT_ROOT / "Votingapp.py")).run()
    app.radio("mode").set_value("Local blockchain (legacy)").run()
    assert not app.exception
    assert "SMART_CONTRACT_ADDRESS" in app.error[0].value
