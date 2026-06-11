from pathlib import Path
import sys

from flask import Flask, jsonify, render_template, request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.query import answer_question

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "")
    return jsonify({"answer": answer_question(question)})


if __name__ == "__main__":
    app.run(debug=True)
