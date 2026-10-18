import os
from pathlib import Path

from flask import Flask, Response

app = Flask(__name__)

LOG_DIR = Path("/var/log/app")
LOG_PATH = LOG_DIR / "visitas.log"


@app.get("/")
def home():
    student_name = os.getenv("STUDENT_NAME", "Carlos")
    barrio = os.getenv("BARRIO", "El Troncal")
    message = f"Hola, I am {student_name} and I live in {barrio}"

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{message}\n")

    return Response(message, mimetype="text/plain")


@app.get("/health")
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
