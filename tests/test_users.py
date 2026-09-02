import pytest
from fastapi.testclient import TestClient
from main import app
from routers.users import usuarios
from models.users import User

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_users():
    """Reinicia la lista de usuarios antes de cada test para aislar el estado."""
    usuarios.clear()
    usuarios.extend(
        [
            User(id=1, name="Luciano Diaz", is_active=True),
            User(id=2, name="Ana Lopez", is_active=True),
            User(id=3, name="Carlos Gomez", is_active=False),
        ]
    )


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "docs" in data
    assert data["docs"] == "/docs"


def test_get_users_all():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) == 3


def test_get_users_filter_active():
    response = client.get("/users?is_active=true")
    assert response.status_code == 200
    users = response.json()["users"]
    assert len(users) == 2
    assert all(u["is_active"] is True for u in users)


def test_get_users_filter_inactive():
    response = client.get("/users?is_active=false")
    assert response.status_code == 200
    users = response.json()["users"]
    assert len(users) == 1
    assert users[0]["id"] == 3
    assert users[0]["is_active"] is False


def test_get_user_by_id_success():
    response = client.get("/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["name"] == "Luciano Diaz"
    assert user["is_active"] is True


def test_get_user_by_id_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]


def test_create_user_success():
    payload = {"id": 4, "name": "Maria Becerra", "is_active": True}
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["name"] == "Maria Becerra"
    assert data["is_active"] is True
    assert "mensaje" in data or "message" in data

    # Verificar que ahora esté en la lista
    get_res = client.get("/users/4")
    assert get_res.status_code == 200


def test_create_user_duplicate_id():
    payload = {"id": 1, "name": "Duplicado", "is_active": True}
    response = client.post("/users", json=payload)
    assert response.status_code == 400
    assert "ya existe" in response.json()["detail"]


def test_update_user_put():
    payload = {"name": "Luciano D. Modificado", "is_active": False}
    response = client.put("/users/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Luciano D. Modificado"
    assert data["is_active"] is False
    assert "modificado" in data["message"].lower()

    # Verificar persistencia en memoria
    get_res = client.get("/users/1")
    assert get_res.json()["name"] == "Luciano D. Modificado"
    assert get_res.json()["is_active"] is False


def test_update_user_patch():
    payload = {"name": "Solo Nombre Actualizado"}
    response = client.patch("/users/2", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Solo Nombre Actualizado"
    assert data["is_active"] is True


def test_update_user_not_found():
    payload = {"name": "Fantasma", "is_active": True}
    response = client.put("/users/999", json=payload)
    assert response.status_code == 404


def test_delete_user_success():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert "eliminado correctamente" in response.json()["message"]

    # Verificar que ya no existe
    get_res = client.get("/users/1")
    assert get_res.status_code == 404


def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]


def test_user_singular_alias():
    # Verifica compatibilidad con endpoint /user de la cátedra
    response = client.get("/user")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 3
