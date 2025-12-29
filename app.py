from flask import Flask, request, jsonify, send_from_directory
from utils import check_expiry, check_recall

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/message", methods=["POST"])
def message():
    text = request.json.get("message", "").lower()

    # STORAGE QUESTIONS
    if "store" in text:
        if "insulin" in text:
            return jsonify({"reply":
                "Store insulin in a refrigerator (2–8°C). Do not freeze. "
                "Once opened, it can stay at room temperature for up to 28 days. "
                "Keep away from sunlight and heat."
            })

        return jsonify({"reply":
            "Most medicines should be stored in a cool, dry place, "
            "away from sunlight and moisture."
        })

    # GENERIC HEALTH QUESTIONS
    if "what is" in text or "can i" in text:
        return jsonify({"reply":
            "I can help with medicine safety, storage, expiry, and recalls. "
            "For diagnosis or treatment decisions, consult a healthcare professional."
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
        response += "Please provide batch number or expiry date for a safety check."

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
