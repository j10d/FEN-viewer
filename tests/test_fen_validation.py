import pytest

from fen_viewer.fen_validation import validate_fen

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
SCHOLARS_MATE_FEN = "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
EMPTY_BOARD_FEN = "8/8/8/8/8/8/8/8 w - - 0 1"
PIECE_PLACEMENT_ONLY = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class TestValidFEN:
    def test_starting_position(self) -> None:
        board = validate_fen(STARTING_FEN)
        assert board is not None

    def test_scholars_mate(self) -> None:
        board = validate_fen(SCHOLARS_MATE_FEN)
        assert board is not None

    def test_empty_board(self) -> None:
        board = validate_fen(EMPTY_BOARD_FEN)
        assert board is not None

    def test_piece_placement_only(self) -> None:
        """A FEN with only the piece placement field should be accepted."""
        board = validate_fen(PIECE_PLACEMENT_ONLY)
        assert board is not None


class TestInvalidFEN:
    def test_empty_string(self) -> None:
        with pytest.raises(ValueError, match="FEN string must not be empty"):
            validate_fen("")

    def test_nonsense_string(self) -> None:
        with pytest.raises(ValueError):
            validate_fen("not a fen string")

    def test_wrong_number_of_ranks(self) -> None:
        with pytest.raises(ValueError):
            validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP")

    def test_invalid_piece_character(self) -> None:
        with pytest.raises(ValueError):
            validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBXKBNR w KQkq - 0 1")

    def test_whitespace_only(self) -> None:
        with pytest.raises(ValueError):
            validate_fen("   ")
