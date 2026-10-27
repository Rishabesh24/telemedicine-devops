
from flask import Flask, request
from html import escape

app = Flask(__name__)
visits = []


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Telemedicine V2</title></head>
    <body>
      <h1>Telemedicine System - V2</h1>
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

      <p><a href="/history">View Past Visits</a></p>
      <p>Version 2: Booking + History</p>
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

    return """
    <h2>Visit booked successfully!</h2>
    <a href="/history">View Visit History</a> |
    <a href="/">Home</a>
    """


@app.route("/history")
def history():
    if not visits:
        return "<h2>No visits found</h2><a href='/'>Home</a>"

    rows = ""
    for visit in visits:
        rows += (
            "<tr>"
            f"<td>{visit['id']}</td>"
            f"<td>{escape(visit['patient'])}</td>"
            f"<td>{escape(visit['doctor'])}</td>"
            f"<td>{escape(visit['date'])}</td>"
            "</tr>"
        )

    return f"""
    <h1>Past Telemedicine Visits - V2</h1>
    <table border="1" cellpadding="8">
      <tr>
        <th>ID</th><th>Patient</th><th>Doctor</th><th>Date</th>
      </tr>
      {rows}
    </table>
    <p><a href="/">Home</a></p>
    """


@app.route("/health")
def health():
    return {"status": "healthy", "version": "v2"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
