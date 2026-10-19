import json

from students.carlos.app import app as flask_app


def test_root_returns_expected_message_and_logs_visit(monkeypatch, tmp_path):
    log_dir = tmp_path / "var" / "log" / "app"
    log_path = log_dir / "visitas.log"

    monkeypatch.setenv("STUDENT_NAME", "Carlos")
    monkeypatch.setenv("BARRIO", "El Troncal")
    monkeypatch.setattr("students.carlos.app.LOG_DIR", log_dir)
    monkeypatch.setattr("students.carlos.app.LOG_PATH", log_path)

    client = flask_app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Hola, I am Carlos and I live in El Troncal"
    assert response.mimetype == "text/plain"
    assert log_path.read_text(encoding="utf-8").strip() == "Hola, I am Carlos and I live in El Troncal"


def test_health_returns_ok(monkeypatch):
    monkeypatch.delenv("STUDENT_NAME", raising=False)
    monkeypatch.delenv("BARRIO", raising=False)

    client = flask_app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert json.loads(response.data) == {"ok": True}
