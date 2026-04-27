---
description: "Fix all type-checking errors using mypy and create a pull request"
agent: "MypyFixer"
argument-hint: "Run mypy type checks and create PR"
---

# Autonomous Type Error Fixer

Fix all type-checking errors in the app directory and create a pull request:

1. Run `uv run mypy app --strict` to identify all type errors
2. Fix errors iteratively, prioritizing the lowest-hanging fruit first
3. Add proper type hints (e.g., `list[str]`, `dict[str, Any]`, `-> None`) instead of generic `# type: ignore`
4. Run `uv run mypy app --strict` again after each fix to verify
5. Commit changes with conventional commit messages prefixed with `fix(types):`
6. Create a new pull request with a clear description of the changes

**Success criteria**: `uv run mypy app --strict` exits with zero errors and PR is created.
