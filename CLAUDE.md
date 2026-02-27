# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FEN-viewer is a Python web application that renders chess board images from positions specified in FEN (Forsyth-Edwards Notation).

## Tech Stack

- **Python** with the `python-chess` library for FEN parsing and board representation
- **Flask** for the web layer
- **pytest** for testing
- SVG output via `chess.svg`

## Architecture

Three-module design in `fen_viewer/`:
- `fen_validation.py` — `validate_fen(fen: str) -> chess.Board`: validates FEN input, raises `ValueError` on invalid input
- `board_renderer.py` — `render_board_svg(board: chess.Board) -> str`: renders a board to SVG string
- `app.py` — `create_app() -> Flask`: Flask app factory with routes `GET /` (starting position) and `GET /board?fen=<fen>`

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
pytest tests/test_fen_validation.py

# Run a single test
pytest tests/test_fen_validation.py::TestValidFEN::test_starting_position

# Install dependencies
pip install -e ".[dev]"

# Run the dev server
flask --app fen_viewer.app run

# Run tests with verbose output
pytest -v
```
