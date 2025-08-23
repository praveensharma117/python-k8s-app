from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify(message="Hello from Flask v2.2 + Werkzeug 2.2, via Gunicorn!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

