from app import app


def test_home_page():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Book a Telemedicine Visit" in response.data


def test_booking():
    response = app.test_client().post(
        "/book",
        data={
            "patient": "Test Patient",
            "doctor": "Test Doctor",
            "date": "2026-11-01"
        }
    )
    assert response.status_code == 200
    assert b"Visit booked successfully" in response.data


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["version"] == "v1"