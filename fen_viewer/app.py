from flask import Flask, Response, request
from markupsafe import Markup

from fen_viewer.board_renderer import render_board_svg
from fen_viewer.fen_validation import validate_fen

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FEN Viewer</title>
<style>
  body {{ font-family: sans-serif; max-width: 500px; margin: 2rem auto; text-align: center; }}
  #board {{ margin: 0 auto 1rem; }}
  #fen {{ width: 100%; font-family: monospace; font-size: 0.9rem; box-sizing: border-box; }}
  #error {{ color: red; margin-top: 0.5rem; }}
  button {{ margin-top: 0.5rem; }}
</style>
</head>
<body>
<div id="board">{board_svg}</div>
<input id="fen" type="text" value="{starting_fen}">
<div>
  <button id="submit-btn" type="button">Submit</button>
  <button id="reset-btn" type="button">Reset</button>
</div>
<div id="error"></div>
<script>
const DEFAULT_FEN = "{starting_fen}";
const boardEl = document.getElementById("board");
const fenEl = document.getElementById("fen");
const errorEl = document.getElementById("error");

document.getElementById("submit-btn").addEventListener("click", async () => {{
  errorEl.textContent = "";
  const resp = await fetch("/board?fen=" + encodeURIComponent(fenEl.value));
  if (resp.ok) {{
    boardEl.innerHTML = await resp.text();
  }} else {{
    errorEl.textContent = await resp.text();
  }}
}});

document.getElementById("reset-btn").addEventListener("click", async () => {{
  fenEl.value = DEFAULT_FEN;
  errorEl.textContent = "";
  const resp = await fetch("/board?fen=" + encodeURIComponent(DEFAULT_FEN));
  if (resp.ok) {{
    boardEl.innerHTML = await resp.text();
  }}
}});
</script>
</body>
</html>"""


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        board = validate_fen(STARTING_FEN)
        svg = render_board_svg(board)
        return INDEX_HTML.format(board_svg=Markup(svg), starting_fen=STARTING_FEN)

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
