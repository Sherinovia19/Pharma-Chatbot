from flask import Flask, request, jsonify, render_template
from utils import (
    normalize_medicine_name,
    extract_batch,
    parse_date,
    check_expiry,
    check_recalled
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/message", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").lower().strip()

    # ---------- STORAGE QUESTIONS ----------
    if "store" in user_msg or "storage" in user_msg:
        if "insulin" in user_msg:
            return jsonify({
                "reply": (
                    "🧊 **Insulin Storage Guidelines**\n\n"
                    "- Refrigerate unopened insulin (2°C–8°C)\n"
                    "- Never freeze insulin\n"
                    "- Opened insulin lasts up to 28 days at room temperature\n"
                    "- Keep away from heat and sunlight\n\n"
                    "_Always follow manufacturer instructions._"
                )
            })

        return jsonify({
            "reply": (
                "🌡️ **General Medicine Storage Advice**\n\n"
                "- Store in a cool, dry place\n"
                "- Avoid moisture and sunlight\n"
                "- Keep medicines out of reach of children\n\n"
                "_Consult a pharmacist for special medicines._"
            )
        })

    # ---------- MEDICINE CHECK ----------
    medicine = normalize_medicine_name(user_msg)
    batch = extract_batch(user_msg)
    expiry = parse_date(user_msg)

    if not medicine:
        return jsonify({
            "reply": (
                "Please mention a medicine name.\n\n"
                "Example:\n"
                "`Check Paracetamol batch PX-101 expiry 2026-05-20`"
            )
        })

    reply = f"💊 **Medicine:** {medicine.title()}\n\n"

    recalled = check_recalled(medicine, batch)
    if recalled:
        reply += (
            f"🚨 **Recall Alert**\n"
            f"Batch `{batch}` is recalled.\n"
            f"Reason: {recalled['reason']}\n\n"
        )
    else:
        reply += "✅ **No recall found for this batch**\n\n"

    if expiry:
        status = check_expiry(expiry)
        if status == "expired":
            reply += "❌ **Expired — Do NOT use**\n\n"
        elif status == "near_expiry":
            reply += "⚠️ **Near expiry — Use soon**\n\n"
        else:
            reply += "✅ **Safe to use**\n\n"

    reply += (
        "🌡️ **Storage Advice**\n"
        "- Cool, dry place\n"
        "- Away from sunlight\n"
        "- Keep out of reach of children\n\n"
        "_AI-generated info. Consult a pharmacist._"
    )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

