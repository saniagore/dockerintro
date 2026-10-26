import json
from datetime import datetime

from students.juan.app import app as flask_app


def test_root_uses_defaults_and_logs_timestamped_visit(monkeypatch, tmp_path):
    log_dir = tmp_path / "var" / "log" / "app"
    log_path = log_dir / "visitas.log"

    monkeypatch.delenv("STUDENT_NAME", raising=False)
    monkeypatch.delenv("BARRIO", raising=False)
    monkeypatch.setattr("students.juan.app.LOG_DIR", log_dir)
    monkeypatch.setattr("students.juan.app.LOG_PATH", log_path)

    client = flask_app.test_client()
    response = client.get("/")
    second_response = client.get("/")

    message = "Hi, I am Juan Diego and I live in Mariano Ramos"
    assert response.status_code == 200
    assert response.get_data(as_text=True) == message
    assert response.mimetype == "text/plain"
    assert second_response.status_code == 200

    entries = log_path.read_text(encoding="utf-8").splitlines()
    assert len(entries) == 2
    for entry in entries:
        timestamp, logged_message = entry.split(" ", 1)
        assert datetime.fromisoformat(timestamp).tzinfo is not None
        assert logged_message == message


def test_root_uses_environment_variables(monkeypatch, tmp_path):
    log_path = tmp_path / "visitas.log"
    monkeypatch.setenv("STUDENT_NAME", "Juan")
    monkeypatch.setenv("BARRIO", "Mariano Ramos")
    monkeypatch.setattr("students.juan.app.LOG_DIR", tmp_path)
    monkeypatch.setattr("students.juan.app.LOG_PATH", log_path)

    response = flask_app.test_client().get("/")

    assert response.get_data(as_text=True) == "Hi, I am Juan and I live in Mariano Ramos"
    assert log_path.read_text(encoding="utf-8").strip().endswith(
        "Hi, I am Juan and I live in Mariano Ramos"
    )


def test_health_returns_ok():
    response = flask_app.test_client().get("/health")

    assert response.status_code == 200
    assert json.loads(response.data) == {"ok": True}
