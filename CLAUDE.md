# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FEN-viewer is a Python web application that renders chess board images from positions specified in FEN (Forsyth-Edwards Notation).

## Tech Stack

- **Python** with the `python-chess` library for FEN parsing and board representation
- **pytest** for testing

## Development Approach

This project follows **test-driven development (TDD)**. Write comprehensive tests before implementation code.

## Code Style

- Use modern Python type annotations (Python 3.10+ syntax):
  - `X | Y` instead of `Union[X, Y]` (PEP 604)
  - `list[str]`, `dict[str, int]` instead of `List[str]`, `Dict[str, int]` (PEP 585)
  - `str | None` instead of `Optional[str]`

## Commands

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_example.py

# Run a single test
pytest tests/test_example.py::test_function_name

# Run tests with verbose output
pytest -v
```
