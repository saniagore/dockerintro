import datetime
import os
from pathlib import Path

from fastapi import FastAPI, Request, Response

app = FastAPI()

LOG_DIR = Path("/var/log/app")
LOG_PATH = LOG_DIR / "visitas.log"


@app.get("/")
async def root(request: Request) -> Response:
    student_name = os.getenv("STUDENT_NAME", "Santiago")
    barrio = os.getenv("BARRIO", "Bulevar del Río")
    message = f"Hola, I am {student_name} and I live in {barrio}"

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} {message}\n")

    return Response(content=message, media_type="text/plain; charset=utf-8")


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
