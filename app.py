from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/message", methods=["POST"])
def message():
    data = request.get_json()
    text = data.get("message", "").lower()

    if "hi" in text or "hello" in text:
        reply = "👋 Hello! I’m MedCheck AI 🩺 How can I help you today?"
    elif "expiry" in text:
        reply = "⏳ Always check medicine expiry. Expired medicines can be unsafe."
    elif "tablet" in text:
        reply = "💊 Tablets usually last 2–3 years if stored properly."
    elif "syrup" in text:
        reply = "🥄 Syrups expire faster after opening (1–3 months)."
    elif "storage" in text:
        reply = "🏥 Store medicines in a cool, dry place away from sunlight."
    elif "pain" in text:
        reply = "🩹 Paracetamol is commonly used for pain, but don’t exceed dosage."
    else:
        reply = "🩺 I can help with medicine expiry, storage, and safety advice."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
