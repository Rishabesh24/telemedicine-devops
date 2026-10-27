from app import app


def test_home_has_features():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"View Past Visits" in response.data
    assert b"Consultation Notes" in response.data


def test_booking_history_and_notes():
    client = app.test_client()

    client.post("/book", data={
        "patient": "Test Patient",
        "doctor": "Test Doctor",
        "date": "2026-11-01"
    })

    response = client.get("/history")
    assert response.status_code == 200
    assert b"Test Patient" in response.data

    response = client.post(
        "/notes/1",
        data={"notes": "Follow-up consultation required"},
        follow_redirects=True
    )
    assert response.status_code == 200

    response = client.get("/history")
    assert b"Follow-up consultation required" in response.data


def test_unknown_visit():
    response = app.test_client().get("/notes/999")
    assert response.status_code == 404


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["version"] == "v3"