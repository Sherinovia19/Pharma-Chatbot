from flask import Flask, render_template, request, jsonify
import json, re
from utils import check_expiry

app = Flask(__name__)

# Load medicine database
try:
    with open("medicine_db.json") as f:
        MED_DB = json.load(f)
except Exception as e:
    MED_DB = {}
    print("Error loading medicine_db.json:", e)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/message", methods=["POST"])
def message():
    try:
        text = request.json.get("message", "").lower().strip()
        if not text:
            return jsonify({"reply": "⚠️ Please enter a message."})

        # Greeting
        if re.search(r"\b(hi|hello|hey)\b", text):
            return jsonify({"reply":
                "👋 Hello! I’m <b>MedCheck AI</b> 🩺<br>"
                "You can check medicine expiry, batch safety, or medicine details."
            })

        # Expiry check
        match = re.search(
            r"check\s+([a-zA-Z]+)\s+batch\s+([a-zA-Z0-9\-]+)\s+(\d{2}/\d{2}/\d{4})",
            text
        )
        if match:
            med, batch, date = match.groups()
            status, days = check_expiry(date)
            med = med.capitalize()

            if status == "expired":
                reply = f"❌ <b>{med}</b> (Batch {batch}) is <b>EXPIRED</b>.<br>Expired {days} days ago."
            elif status == "expiring_soon":
                reply = f"⚠️ <b>{med}</b> (Batch {batch}) is <b>EXPIRING SOON</b>.<br>{days} days remaining."
            elif status == "valid":
                reply = f"✅ <b>{med}</b> (Batch {batch}) is <b>SAFE</b>.<br>Valid for {days} days."
            else:
                reply = "⚠️ Invalid date format. Use DD/MM/YYYY."

            return jsonify({"reply": reply})

        # Medicine lookup
        for med in MED_DB:
            if med in text:
                info = MED_DB[med]
                return jsonify({"reply":
                    f"💊 <b>{med.capitalize()}</b><br>"
                    f"<b>Use:</b> {info['use']}<br>"
                    f"<b>Adult dose:</b> {info['adult_dose']}<br>"
                    f"<b>Child dose:</b> {info['child_dose']}<br>"
                    f"<b>Warning:</b> {info['warnings']}"
                })

        # Storage advice
        if "storage" in text:
            return jsonify({"reply":
                "🏥 <b>Medicine Storage Tips</b><br>"
                "• Store in a cool, dry place<br>"
                "• Avoid sunlight & moisture<br>"
                "• Refrigerate only if instructed<br>"
                "• Keep away from children"
            })

        # Default reply
        return jsonify({"reply":
            "🩺 I can help with:<br>"
            "• Medicine expiry checks<br>"
            "• Batch safety<br>"
            "• Dosage & warnings<br><br>"
            "<b>Example:</b><br>"
            "Check paracetamol batch ABC-123 29/12/2025"
        })
    except Exception as e:
        print("Error in /api/message:", e)
        return jsonify({"reply": "⚠️ Oops! Something went wrong. Try again."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
