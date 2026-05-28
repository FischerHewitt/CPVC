Run the backend test suite and confirm all tests pass. Covers step 9 of the add-major checklist.

## What to do

Run pytest from the backend directory using the project's virtual environment:

```bash
cd backend && .venv/bin/pytest
```

If any tests fail:
- Read the failure output carefully
- Fix the root cause in the relevant file (`flowcharts.py`, `concentrations.py`, `electives.py`, or the test file itself)
- Re-run until all tests pass

Do not skip or comment out failing tests. Do not use `pytest -k` to filter them out. Every test must pass before moving on.

Once all tests pass, report the final test count and confirm success.
