# GitHub Copilot Instructions for github-copilot-training Repository

## High-Level Details

This repository is a training project for GitHub Copilot, featuring a simple FastAPI-based Productivity Reporting System. It demonstrates task management and productivity metrics for developers. The project is small in size (approximately 10-20 files), written in Python, and uses modern asynchronous web frameworks. It serves as an educational tool with 7 training modules covering Copilot usage.

Primary language: Python 3.12
Framework: FastAPI with Uvicorn
Dependency management: uv (via pyproject.toml)
Data validation: Pydantic
Testing: pytest with pytest-asyncio
Type checking: mypy

## Build Instructions

### Bootstrap
To set up the development environment:
1. Ensure Python 3.12 is installed.
2. Install uv: `pip install uv` (if not already installed; uv version 0.11.7 or later recommended).
3. In the repository root, run `uv sync` to install all dependencies. This command resolves and installs packages from pyproject.toml, including dev dependencies like pytest and mypy. It takes about 2-5 seconds on a typical machine.

Preconditions: Python 3.12.*, internet connection for package downloads.
Postconditions: A .venv/ directory is created with the virtual environment, and all packages are installed.

### Build
No explicit build step is required, as this is a pure Python project without compilation. The "build" is effectively the dependency installation via `uv sync`.

### Test
To run tests:
1. After `uv sync`, run `uv run pytest` from the repository root.
2. This discovers and runs all test files in the `tests/` directory.
3. Currently, no tests exist, so it reports "collected 0 items" and exits with code 1 (no tests found is considered a failure in pytest by default).

Order: Always run `uv sync` before `uv run pytest` to ensure test dependencies (pytest, pytest-asyncio) are available.
Time: Less than 1 second when no tests are present.

Validation: Tests should pass without errors. If tests fail, check for import issues or missing dependencies.

### Run
To start the application:
1. Run `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000` from the repository root.
2. The server starts on http://127.0.0.1:8000, with Swagger UI at /docs.

Preconditions: Dependencies installed via `uv sync`.
Postconditions: Server is running and accessible. It binds to port 8000; ensure the port is free.

For development with auto-reload: Add `--reload` flag, but note it may consume more resources.

Errors observed: If port 8000 is in use, binding fails with "only one usage of each socket address... permitted". Workaround: Use a different port with `--port <new_port>` or kill the conflicting process.

### Lint
To check types and code quality:
1. Run `uv run mypy app/` from the repository root.
2. mypy checks type hints in the app/ directory.

Time: About 2-5 seconds.
Postconditions: Reports "Success: no issues found" if types are correct.

No other linting tools are configured.

### Other Scripted Steps
- No additional scripts in pyproject.toml or elsewhere.
- No CI/CD pipelines (no .github/workflows directory).

Environment setup: The project uses uv for isolation; no global installs required. The .venv/ is gitignored.

Validation steps: After changes, always run `uv run mypy app/` and `uv run pytest` to ensure no regressions. For API changes, start the server and test endpoints manually or via /docs.

Making a change: Edited app/main.py to add a new field; no build issues occurred. Ran mypy and pytest successfully.

## Project Layout

### Architectural Elements
- Main application: `app/main.py` - Contains FastAPI app initialization, Pydantic models (TaskStatus, DeveloperTask, ProductivityReport), mock database (MOCK_TASKS dict), async functions for data fetching, and API routes (/status, /tasks, /report, /log_task).
- Configuration: `pyproject.toml` - Defines project metadata, dependencies (fastapi[standard], uvicorn[standard], httpx, mypy), dev dependencies (pytest, pytest-asyncio), and uv settings.
- Tests: `tests/` directory (currently empty except __init__.py).
- Documentation: `trainings-tasks/` with 7 .md files for training modules.
- Root files: README.md (overview and setup), .gitignore (Python standard), uv.lock (locked dependency versions).

No separate config files for linting/compilation; mypy runs without config.

### Checks Prior to Check-in
No GitHub workflows or CI builds. No continuous integration pipelines.

Validation pipelines: Manual - run mypy and pytest before committing.

Steps to replicate: Run `uv run mypy app/` and `uv run pytest` locally.

Explicit validation: Ensure API endpoints return correct models; test via Swagger UI or httpx in tests.

Dependencies: All listed in pyproject.toml; no hidden deps. Uses standard libraries implicitly.

### Key Files and Snippets
Repository root files:
- pyproject.toml
- README.md
- .gitignore
- uv.lock
- .venv/ (created by uv sync, gitignored)

Contents of README.md: Overview of the project as a FastAPI app for training, tech stack (Python 3.10+, FastAPI, uv, Pydantic), training modules, prerequisites (uv, VS Code, Copilot), getting started commands.

Contents of pyproject.toml: Project name "app", Python 3.12.*, dependencies including FastAPI, uvicorn, httpx, mypy; dev group with pytest.

Contents of app/main.py: Imports, enums/models, mock data, async functions, FastAPI app and routes.

Snippet from app/main.py:
```python
app = FastAPI(title="Productivity Reporting System")

@app.get("/status")
def get_status():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[DeveloperTask])
async def get_all_tasks():
    return await fetch_all_tasks()
```

No other source files in app/.

Tests directory: Only __init__.py.

Trainings-tasks: 7 .md files with training content.

Trust these instructions; only search if incomplete or erroneous.