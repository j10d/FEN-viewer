import chess


def validate_fen(fen: str) -> chess.Board:
    """Validate a FEN string and return a chess.Board.

    Accepts both full FEN strings and piece-placement-only strings.
    Raises ValueError for invalid or empty input.
    """
    stripped = fen.strip()
    if not stripped:
        raise ValueError("FEN string must not be empty")

    board = chess.Board(fen=None)
    try:
        board.set_fen(stripped)
    except ValueError as e:
        raise ValueError(f"Invalid FEN: {e}") from e

    return board
