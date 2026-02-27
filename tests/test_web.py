import pytest
from flask.testing import FlaskClient

from fen_viewer.app import create_app

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


class TestBoardEndpoint:
    def test_valid_fen_returns_svg(self, client: FlaskClient) -> None:
        response = client.get("/board", query_string={"fen": STARTING_FEN})
        assert response.status_code == 200
        assert response.content_type == "image/svg+xml"
        assert b"<svg" in response.data

    def test_invalid_fen_returns_400(self, client: FlaskClient) -> None:
        response = client.get("/board", query_string={"fen": "not a fen"})
        assert response.status_code == 400

    def test_missing_fen_returns_400(self, client: FlaskClient) -> None:
        response = client.get("/board")
        assert response.status_code == 400

    def test_empty_fen_returns_400(self, client: FlaskClient) -> None:
        response = client.get("/board", query_string={"fen": ""})
        assert response.status_code == 400


class TestIndexPage:
    def test_index_returns_html(self, client: FlaskClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.content_type

    def test_index_contains_chess_board(self, client: FlaskClient) -> None:
        response = client.get("/")
        assert b"<svg" in response.data

    def test_index_contains_fen_input(self, client: FlaskClient) -> None:
        response = client.get("/")
        assert b"<input" in response.data

    def test_index_input_prefilled_with_starting_fen(self, client: FlaskClient) -> None:
        response = client.get("/")
        assert STARTING_FEN.encode() in response.data

    def test_index_contains_submit_button(self, client: FlaskClient) -> None:
        response = client.get("/")
        html = response.data.decode()
        assert "submit" in html.lower() or "Submit" in html

    def test_index_contains_reset_button(self, client: FlaskClient) -> None:
        response = client.get("/")
        html = response.data.decode()
        assert "reset" in html.lower() or "Reset" in html

    def test_index_contains_default_fen_in_script(self, client: FlaskClient) -> None:
        """The page JS should include the starting FEN so the reset button can use it."""
        response = client.get("/")
        html = response.data.decode()
        assert "<script" in html
        assert STARTING_FEN in html
