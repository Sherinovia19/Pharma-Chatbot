from flask import Flask, request, jsonify, send_from_directory
from utils import check_expiry, check_recall
import os

app = Flask(__name__, static_folder="static")

# Serve UI
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# Chat API
@app.route("/api/message", methods=["POST"])
def chat():
    text = request.json.get("message", "").lower()

    # STORAGE QUESTIONS
    if "store" in text:
        if "insulin" in text:
            return jsonify({
                "reply": (
                    "Store insulin in a refrigerator at 2–8°C. "
                    "Do not freeze. Once opened, it can be kept at room "
                    "temperature for up to 28 days. Keep away from heat and sunlight."
                )
            })
        return jsonify({
            "reply": (
                "Most medicines should be stored in a cool, dry place, "
                "away from sunlight and moisture."
            )
        })

    # GENERIC QUESTIONS
    if "what is" in text or "can i" in text:
        return jsonify({
            "reply": (
                "I can help with medicine safety, expiry checks, recalls, "
                "and storage guidance. For diagnosis or treatment decisions, "
                "please consult a healthcare professional."
            )
        })

    # MEDICINE CHECK
    med = ""
    batch = ""
    expiry = ""

    parts = text.split(",")
    for p in parts:
        if "batch" in p:
            batch = p.split(":")[-1].strip()
        elif "expiry" in p:
            expiry = p.split(":")[-1].strip()
        else:
            med = p.strip()

    if not med:
        return jsonify({
            "reply": "Please mention a medicine name to proceed."
        })

    response = f"Medicine: {med.title()}.\n"

    if batch:
        recall = check_recall(med, batch)
        if recall:
            response += f"⚠️ This batch is recalled due to {recall}.\n"
        else:
            response += "✅ No recall found for this batch.\n"

    if expiry:
        status = check_expiry(expiry)
        if status == "expired":
            response += "❌ This medicine is expired. Do not use."
        elif status == "near":
            response += "⚠️ This medicine is near expiry. Use cautiously."
        elif status == "safe":
            response += "✅ This medicine is safe to use."

    if not batch and not expiry:
        response += "Please provide a batch number or expiry date."

    return jsonify({"reply": response})

# REQUIRED FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
