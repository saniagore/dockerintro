import datetime
import os
from pathlib import Path

from flask import Flask, Response, jsonify

app = Flask(__name__)
LOG_DIR = Path("/var/log/app")
LOG_PATH = LOG_DIR / "visitas.log"


@app.get("/")
def home() -> Response:
    student_name = os.getenv("STUDENT_NAME", "Daniel")
    barrio = os.getenv("BARRIO", "San Luis II")
    message = f"Hola, I am {student_name} and I live in {barrio}"

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} {message}\n")

    return Response(message, mimetype="text/plain")


@app.get("/health")
def health():
    return jsonify(ok=True), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
