from fastapi.testclient import TestClient
from .main import app

# Creamos el cliente de pruebas
client = TestClient(app)

def test_read_main():
    """Prueba que el endpoint raíz funcione"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Online", "environment": "Development"}

def test_create_note_positive():
    """Prueba la lógica de sentimiento positivo"""
    response = client.post(
        "/notes",
        json={"title": "Test DevOps", "content": "Este es un excelente proyecto"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Positivo"
    assert "id" in data

def test_create_note_negative():
    """Prueba la lógica de sentimiento negativo"""
    response = client.post(
        "/notes",
        json={"title": "Error fatal", "content": "Hay un fallo terrible en el sistema"}
    )
    assert response.status_code == 200
    assert response.json()["sentiment"] == "Negativo"