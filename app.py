from flask import Flask, render_template, request, jsonify
from utils import check_expiry, check_recall
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/message", methods=["POST"])
def chat():
    text = request.json.get("message", "").lower()

    # Storage questions
    if "store" in text:
        if "insulin" in text:
            return jsonify({
                "reply": "Store insulin in a refrigerator (2–8°C). Do not freeze. Once opened, it can be kept at room temperature for up to 28 days."
            })
        return jsonify({
            "reply": "Most medicines should be stored in a cool, dry place away from sunlight and moisture."
        })

    # Generic fallback
    if not text.strip():
        return jsonify({"reply": "Please ask a medicine-related question."})

    med, batch, expiry = "", "", ""

    parts = text.split(",")
    for p in parts:
        if "batch" in p:
            batch = p.split(":")[-1].strip()
        elif "expiry" in p:
            expiry = p.split(":")[-1].strip()
        else:
            med = p.strip()

    response = f"Medicine: {med.title()}\n"

    if batch:
        recall = check_recall(med, batch)
        response += "⚠️ Recalled batch detected.\n" if recall else "✅ No recall found.\n"

    if expiry:
        status = check_expiry(expiry)
        if status == "expired":
            response += "❌ This medicine is expired."
        elif status == "near":
            response += "⚠️ This medicine is nearing expiry."
        else:
            response += "✅ This medicine is safe to use."

    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

