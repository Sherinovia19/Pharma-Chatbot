from flask import Flask, request, jsonify, render_template
import utils

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/message", methods=["POST"])
def message():
    try:
        user_input = request.json.get("message", "")
        reply = utils.get_bot_response(user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "⚠️ Bot encountered an error. Please try again."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
