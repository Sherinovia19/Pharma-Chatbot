# app.py
from flask import Flask, request, jsonify, render_template
from utils import parse_date, check_expiry, check_recalled, extract_batch, normalize_medicine_name

app = Flask(__name__)

# Home page
@app.route("/")
def index():
    return render_template("index.html")  # Shows the chat UI

# Endpoint for chat messages
@app.route("/api/message", methods=["POST"])
def message():
    data = request.json or {}
    text = data.get("message", "").strip()
    lower = text.lower()

    # Check for expiry date
    if any(token in lower for token in ["expiry", "exp", "expires"]):
        dt = parse_date(text)
        if not dt:
            return jsonify({"reply": "I couldn't parse the date. Try '2026-03-25'"})
        status = check_expiry(dt)
        reply_map = {
            "expired": "This product is EXPIRED. Do not use it.",
            "near_expiry": "This product is near expiry. Use caution.",
            "ok": "This product is not expired and looks OK."
        }
        return jsonify({"reply": reply_map[status]})

    # Check for batch number
    batch = extract_batch(text)
    med = normalize_medicine_name(text)
    if batch and med:
        recalled = check_recalled(med, batch)
        if recalled:
            return jsonify({"reply": f"Warning: Batch {batch} of {med} is {recalled.get('status')}."})
        return jsonify({"reply": f"No recall found for batch {batch} of {med}."})

    # Storage advice
    if any(w in lower for w in ["store", "storage", "keep"]):
        return jsonify({"reply": "Store tablets in a cool, dry place away from sunlight."})

    # Default reply
    return jsonify({"reply": "Sorry, I didn't understand. Ask like 'Check Paracetamol batch PX-123 exp 2025-03-01'"})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
