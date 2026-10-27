from app import app


def test_booking_page():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"View Past Visits" in response.data


def test_history_page():
    response = app.test_client().get("/history")
    assert response.status_code == 200
    assert b"No visits found" in response.data


def test_book_and_view_history():
    client = app.test_client()

    client.post("/book", data={
        "patient": "Test Patient",
        "doctor": "Test Doctor",
        "date": "2026-11-01"
    })

    response = client.get("/history")
    assert response.status_code == 200
    assert b"Test Patient" in response.data
    assert b"Test Doctor" in response.data


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["version"] == "v2"