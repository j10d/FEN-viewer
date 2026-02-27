import chess
import chess.svg


def render_board_svg(board: chess.Board) -> str:
    """Render a chess board as an SVG string from white's perspective."""
    return chess.svg.board(board, flipped=False)
