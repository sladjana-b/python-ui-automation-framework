## Features
- Pytest-based UI automation
- Page Object Model (POM)

This project uses a simple Page Object Model structure:
- Each page of the application has a dedicated class inside the `pages/` directory.
- Tests interact only with page objects, not raw locators.
- This keeps tests cleaner, reusable, and easier to maintain.

- Reusable fixtures
- Positive & negative login tests
- Inventory validation test
- Clear project layout


## How to run
pip install -r requirements.txt
pytest -v
