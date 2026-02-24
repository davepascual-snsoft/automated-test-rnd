# IRMS Automation Test

End-to-end test suite for the IRMS client using [Playwright](https://playwright.dev/python/) and [pytest](https://pytest.org/).

---

## Project structure

```
test-rnd/
├── conftest.py          # Session fixtures: browser, login/logout lifecycle
├── pytest.ini           # pytest config and CLI options
├── pages/               # Page Object Models
├── utils/               # Reusable UI helpers (combobox, input, calendar)
├── test/
│   ├── table_pit/       # Table Pit CRUD tests (create → edit → delete)
│   └── zone/            # Zone CRUD tests (create → edit)
└── reports/             # Auto-generated HTML test reports
```

---

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv venv
```

### 2. Activate the virtual environment

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browser binaries

```bash
playwright install chrome
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
IRMS_BASE_URL=https://your-irms-instance.com
IRMS_EMAIL=your@email.com
IRMS_PASSWORD=yourpassword
HEADLESS=true   # set to false to watch the browser during tests
```

---

## Running tests

```bash
pytest
```

Each test follows the full E2E lifecycle:
**Login → Test → Logout → Close**

The HTML report is generated automatically after every run:

```
reports/report.html
```

### Run a specific test file

```bash
pytest test/table_pit/test_1_create.py
```

### Run headed (visible browser)

Set `HEADLESS=false` in `.env`, then run `pytest`.

---

## Test execution order

Tests run in this order by default:

| # | Test | Description |
|---|------|-------------|
| 1 | `table_pit/test_1_create` | Create a new Table Pit |
| 2 | `table_pit/test_2_edit` | Edit an existing Table Pit |
| 3 | `table_pit/test_3_delete` | Delete a Table Pit |
| 4 | `zone/test_create` | Create a new Zone |
| 5 | `zone/test_edit` | Edit an existing Zone |

### Skipping a test

Add to the top of a test file to skip the entire file:

```python
import pytest
pytestmark = pytest.mark.skip(reason="not ready yet")
```

Or skip a single test function:

```python
@pytest.mark.skip(reason="not ready yet")
def test_example(page): ...
```
