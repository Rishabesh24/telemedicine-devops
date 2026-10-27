
from flask import Flask, request, redirect, url_for
from html import escape

app = Flask(__name__)
visits = []


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Telemedicine V3</title></head>
    <body>
      <h1>Telemedicine System - V3</h1>
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
      <p>Version 3: Booking + History + Consultation Notes</p>
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
        "date": date,
        "notes": ""
    })

    return (
        "<h2>Visit booked successfully!</h2>"
        "<a href='/history'>View Visit History</a> | "
        "<a href='/'>Home</a>"
    )


@app.route("/history")
def history():
    if not visits:
        return "<h2>No visits found</h2><a href='/'>Home</a>"

    rows = ""
    for visit in visits:
        rows += f"""
        <tr>
          <td>{visit['id']}</td>
          <td>{escape(visit['patient'])}</td>
          <td>{escape(visit['doctor'])}</td>
          <td>{escape(visit['date'])}</td>
          <td>{escape(visit['notes'])}</td>
          <td><a href="/notes/{visit['id']}">Add/Edit Notes</a></td>
        </tr>
        """

    return f"""
    <h1>Past Visits and Consultation Notes - V3</h1>
    <table border="1" cellpadding="8">
      <tr>
        <th>ID</th><th>Patient</th><th>Doctor</th>
        <th>Date</th><th>Notes</th><th>Action</th>
      </tr>
      {rows}
    </table>
    <p><a href="/">Home</a></p>
    """


@app.route("/notes/<int:visit_id>", methods=["GET", "POST"])
def notes(visit_id):
    visit = next(
        (item for item in visits if item["id"] == visit_id),
        None
    )

    if visit is None:
        return "Visit not found.", 404

    if request.method == "POST":
        visit["notes"] = request.form.get("notes", "").strip()
        return redirect(url_for("history"))

    return f"""
    <h1>Add Consultation Notes</h1>
    <p>Patient: {escape(visit['patient'])}</p>
    <p>Doctor: {escape(visit['doctor'])}</p>

    <form method="post">
      <textarea name="notes" rows="6" cols="50">{escape(visit['notes'])}</textarea>
      <br><br>
      <button type="submit">Save Notes</button>
    </form>

    <p><a href="/history">Back to History</a></p>
    """


@app.route("/health")
def health():
    return {"status": "healthy", "version": "v3"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
