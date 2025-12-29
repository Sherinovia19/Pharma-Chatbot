import os
from flask import Flask, request, jsonify, render_template
from utils import get_bot_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/message", methods=["POST"])
def message():
    data = request.get_json()
    user_message = data.get("message", "")
    try:
        reply = get_bot_response(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "⚠️ Bot encountered an error. Please try again."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
