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


class TestDefaultEndpoint:
    def test_root_returns_starting_position(self, client: FlaskClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        assert b"<svg" in response.data
