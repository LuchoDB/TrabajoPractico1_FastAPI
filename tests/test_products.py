import pytest
from fastapi.testclient import TestClient
from main import app
from routers.products import productos
from models.products import Product

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_products():
    """Reinicia la lista de productos antes de cada test para aislar el estado."""
    productos.clear()
    productos.extend(
        [
            Product(
                id=1,
                name="Notebook Lenovo ThinkPad",
                category="Computación",
                price=1250.0,
                stock=15,
                is_active=True,
            ),
            Product(
                id=2,
                name="Mouse Inalámbrico Logitech",
                category="Periféricos",
                price=45.5,
                stock=50,
                is_active=True,
            ),
            Product(
                id=3,
                name="Teclado Mecánico RGB",
                category="Periféricos",
                price=95.0,
                stock=0,
                is_active=False,
            ),
            Product(
                id=4,
                name="Monitor 27 Pulgadas IPS 144Hz",
                category="Monitores",
                price=320.0,
                stock=8,
                is_active=True,
            ),
        ]
    )


def test_get_products_all():
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 4


def test_get_products_filter_category():
    response = client.get("/products?category=Periféricos")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) == 2
    assert all(p["category"] == "Periféricos" for p in products)


def test_get_products_filter_is_active():
    response = client.get("/products?is_active=false")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) == 1
    assert products[0]["id"] == 3


def test_get_products_filter_name_search():
    response = client.get("/products?name=thinkpad")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) == 1
    assert products[0]["id"] == 1


def test_get_products_filter_price_range():
    response = client.get("/products?min_price=50&max_price=350")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) == 2
    assert {p["id"] for p in products} == {3, 4}


def test_get_product_by_id_success():
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == 1
    assert product["name"] == "Notebook Lenovo ThinkPad"
    assert product["price"] == 1250.0


def test_get_product_by_id_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]


def test_create_product_success():
    payload = {
        "id": 5,
        "name": "Auriculares Bluetooth Sony",
        "category": "Audio",
        "price": 180.0,
        "stock": 25,
        "is_active": True,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 5
    assert data["name"] == "Auriculares Bluetooth Sony"
    assert data["category"] == "Audio"
    assert data["price"] == 180.0
    assert data["stock"] == 25
    assert data["is_active"] is True
    assert "exitosamente" in data["message"]

    # Verificar que existe
    get_res = client.get("/products/5")
    assert get_res.status_code == 200


def test_create_product_duplicate_id():
    payload = {
        "id": 1,
        "name": "Producto Repetido",
        "category": "Varios",
        "price": 10.0,
        "stock": 5,
        "is_active": True,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 400
    assert "ya existe" in response.json()["detail"]


def test_create_product_invalid_validation():
    # Precio <= 0 o stock < 0 debe fallar la validación Pydantic
    payload = {
        "id": 10,
        "name": "Producto Inválido",
        "category": "Varios",
        "price": -5.0,
        "stock": -1,
        "is_active": True,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_update_product_put():
    payload = {
        "name": "Notebook Lenovo ThinkPad Pro X1",
        "category": "Computación Premium",
        "price": 1400.0,
        "stock": 10,
        "is_active": True,
    }
    response = client.put("/products/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Notebook Lenovo ThinkPad Pro X1"
    assert data["price"] == 1400.0
    assert "modificado" in data["message"]

    # Verificar persistencia en memoria
    get_res = client.get("/products/1")
    assert get_res.json()["name"] == "Notebook Lenovo ThinkPad Pro X1"


def test_update_product_patch():
    payload = {"price": 50.0}
    response = client.patch("/products/2", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 50.0
    assert data["name"] == "Mouse Inalámbrico Logitech"


def test_update_product_not_found():
    payload = {"name": "No existe"}
    response = client.put("/products/9999", json=payload)
    assert response.status_code == 404


def test_delete_product_success():
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert "eliminado correctamente" in response.json()["message"]

    # Verificar que ya no existe
    get_res = client.get("/products/1")
    assert get_res.status_code == 404


def test_delete_product_not_found():
    response = client.delete("/products/9999")
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]
