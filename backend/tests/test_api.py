from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["mode"] == "mock"


def test_mock_flow():
    assert client.get("/matches/world-cup").status_code == 200
    recommendations = client.post("/recommendations/run-mock")
    assert recommendations.status_code == 200
    assert len(recommendations.json()) > 0
    bankroll = client.get("/bankroll")
    assert bankroll.status_code == 200
    assert bankroll.json()["initial_balance"] == 1000.0


def test_combined_bet_endpoints():
    payload = {
        "match_id": "worldcup_mock_001",
        "offered_combined_odd": 2.2,
        "legs": [
            {"market": "corners", "selection": "Over 7.5 corners", "individual_odd": 1.2, "estimated_probability": 0.78},
            {"market": "h2h", "selection": "Brazil wins", "individual_odd": 1.1, "estimated_probability": 0.82},
        ],
    }
    assert client.post("/bet-builder/evaluate", json=payload).status_code == 200
    rearrange = client.post("/bet-builder/rearrange", json=payload)
    assert rearrange.status_code == 200
    assert len(rearrange.json()["suggestions"]) > 0
