
from flask import Flask, request
from html import escape

app = Flask(__name__)

# Demo-only in-memory storage.
# Records are lost when the application restarts.
visits = []


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Telemedicine V1</title></head>
    <body>
      <h1>Telemedicine System - V1</h1>
      <h2>Book a Telemedicine Visit</h2>

      <form action="/book" method="post">
        <label>Patient name:</label>
        <input name="patient" required><br><br>

        <label>Doctor name:</label>
        <input name="doctor" required><br><br>

        <label>Visit date:</label>
        <input name="date" type="date" required><br><br>

        <button type="submit">Book Visit</button>
      </form>

      <p>Version 1: Appointment Booking</p>
    </body>
    </html>
    """


@app.route("/book", methods=["POST"])
def book():
    patient = request.form.get("patient", "").strip()
    doctor = request.form.get("doctor", "").strip()
    date = request.form.get("date", "").strip()

    if not patient or not doctor or not date:
        return "All fields are required.", 400

    visits.append({
        "id": len(visits) + 1,
        "patient": patient,
        "doctor": doctor,
        "date": date
    })

    return f"""
    <h2>Visit booked successfully!</h2>
    <p>Patient: {escape(patient)}</p>
    <p>Doctor: {escape(doctor)}</p>
    <p>Date: {escape(date)}</p>
    <a href="/">Book another visit</a>
    """


@app.route("/health")
def health():
    return {"status": "healthy", "version": "v1"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
