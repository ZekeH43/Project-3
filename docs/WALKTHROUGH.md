# Code walkthrough and interview preparation

## Read the project in this order

1. **`project_app2.py`:** read `Employee`, `normalize_employee`, and
   `verify_employee`. Follow how text from a form becomes a validated record.
2. **`DemoVotingService`:** follow registration, duplicate checks, and vote
   counting. A dictionary connects token IDs to employees; sets record membership
   efficiently; a list stores counts in candidate order.
3. **`Votingapp.py`:** trace a submitted form through a service call and its
   `try`/`except`/`else` branches. An exception produces an error, and only the
   successful branch displays success.
4. **`tests/test_voting.py` and `tests/test_app.py`:** compare domain tests with
   tests that actually fill in Streamlit forms.
5. **`blockchain.py`:** follow a transaction through submission, mining,
   receipt-status validation, and event decoding.

## Why these choices matter

| Change | Reason |
| --- | --- |
| Text inputs for identifiers | A value such as `0001` must keep its zeroes; very large token IDs must not become imprecise floats. |
| Paths based on `__file__` | Loading a CSV or image should not depend on the terminal's current folder. |
| Exceptions for failures | Returning an error string looked like an ordinary success value in the original interface. |
| Per-session demo service | Streamlit reruns the script after interactions; session state preserves one demo without sharing mutable state among visitors. |
| Separate blockchain adapter | The core rules can be tested without Streamlit, wallets, or a network. |
| Receipt-specific token event | `totalTokens - 1` can refer to another registration when transactions overlap. |
| Synthetic fixtures | A reviewer can reproduce a demonstration without supplying real personal data. |

## Practice explaining a complete request

Register Demo Employee One, then vote for Alice with token `0`:

1. The form collects four strings.
2. `normalize_employee` validates the fields and normalizes formatting.
3. `verify_employee` requires all four fields to match one sample record.
4. `register_voter` checks for a duplicate ID and creates token `0`.
5. The interface displays that token only after registration succeeds.
6. `cast_vote` validates the token and candidate, checks whether the token has
   voted, and increments Alice's count.
7. A second vote raises an error without changing any count.

In local blockchain mode, the original contract implements different, incomplete
rules. Explain that distinction explicitly: passing Python tests does not prove
the contract is secure or verify a deployment.

## Interview questions to answer in your own words

- Why use a set for tokens that have already voted?
- Why are employee IDs stored as strings during validation?
- What caused the original false-success message, and how is it prevented now?
- What is the difference between submitting and confirming a transaction?
- Why can reading a global token counter return the wrong registration's ID?
- What happens when Streamlit reruns the script or the browser session is lost?
- Which tests run real interface logic, and which simulate the network?
- What would need to change for multiple users to share one persistent election?
- Why can a client-side check never repair an unrestricted smart contract?

## Small exercises for the next iteration

1. Add a turnout display using registered-voter and vote counts. Write a test
   for zero registrations before dividing.
2. Add SQLite persistence behind the demo service while preserving its public
   methods. Test that state survives creating a new service instance.
3. Replace SSN-style sample matching with a non-sensitive demonstration code.
   Keep real identity verification outside the scope of the demo.

Before using this project in an interview, run the demo and tests yourself,
explain the changes above, and distinguish your original work, team work, and
assistance received. Avoid claims such as “secure production voting system.”
