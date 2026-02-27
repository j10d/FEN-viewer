from flask import Flask, Response, request

from fen_viewer.board_renderer import render_board_svg
from fen_viewer.fen_validation import validate_fen

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> Response:
        board = validate_fen(STARTING_FEN)
        svg = render_board_svg(board)
        return Response(svg, content_type="image/svg+xml")

    @app.get("/board")
    def board() -> Response | tuple[Response, int]:
        fen = request.args.get("fen")
        if not fen:
            return Response("Missing 'fen' query parameter", status=400)

        try:
            chess_board = validate_fen(fen)
        except ValueError as e:
            return Response(str(e), status=400)

        svg = render_board_svg(chess_board)
        return Response(svg, content_type="image/svg+xml")

    return app
