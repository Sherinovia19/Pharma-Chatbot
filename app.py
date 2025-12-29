import os
from flask import Flask, render_template, request, jsonify
import utils

app = Flask(__name__)

# Home page — serves your lovable HTML UI
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint for chatbot messages
@app.route("/api/message", methods=["POST"])
def message():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "⚠️ Please enter a message."})

    try:
        # Call the bot logic from utils.py
        reply = utils.get_bot_response(user_input)
    except Exception as e:
        # Catch errors to prevent crashes
        reply = "⚠️ Bot encountered an error. Please try again."
        print(f"[ERROR] get_bot_response failed: {e}")

    return jsonify({"reply": reply})

# Run the Flask app (Render requires host=0.0.0.0 and PORT from env)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default 5000
    app.run(host="0.0.0.0", port=port)

