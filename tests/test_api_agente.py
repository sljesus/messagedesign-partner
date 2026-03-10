import os
import sys

from fastapi.testclient import TestClient

# Ensure repo root is on sys.path for local imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from api_agente import app


def test_health():
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}


def test_chat_whatsapp_response():
    with TestClient(app) as client:
        payload = {"mensaje": "Me interesa WhatsApp", "session_id": "t1", "contexto": {}}
        resp = client.post("/chat", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "respuesta" in data
        assert "WhatsApp Business API" in data["respuesta"]


def test_chat_session_continuity():
    with TestClient(app) as client:
        session_id = "t2"
        first = client.post("/chat", json={"mensaje": "Resenas", "session_id": session_id, "contexto": {}})
        assert first.status_code == 200
        follow = client.post("/chat", json={"mensaje": "si, continuar", "session_id": session_id, "contexto": {}})
        assert follow.status_code == 200
        data = follow.json()
        assert "Siguiente paso" in data.get("respuesta", "")
