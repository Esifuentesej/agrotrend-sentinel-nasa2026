import os
import pytest
from app import app, init_db, DB_NAME

@pytest.fixture
def client():
    app.config["TESTING"] = True
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    init_db()
    with app.test_client() as client:
        yield client

def test_redireccion_sin_login(client):
    res = client.get("/")
    assert res.status_code == 302

def test_registro_y_login(client):
    res_reg = client.post("/register", data={
        "username": "investigador_nasa",
        "password": "password123",
        "rol": "analista"
    }, follow_redirects=True)
    assert res_reg.status_code == 200
    assert b"Registro exitoso" in res_reg.data

    res_log = client.post("/login", data={
        "username": "investigador_nasa",
        "password": "password123"
    }, follow_redirects=True)
    assert res_log.status_code == 200
    assert b"AGROTREND SENTINEL" in res_log.data

def test_crud_analisis_climatico(client):
    client.post("/login", data={"username": "admin", "password": "admin123"})

    res_create = client.post("/", data={
        "ciudad_a": "Arequipa - Valle (Perú) | Agropecuario",
        "ciudad_b": "Ica - Valle Costero (Perú) | Agroexportación",
        "auto_redirigir": "on",
        "codigo_var": "PRECTOTCORR",
        "inicio": "2005",
        "fin": "2024",
        "anios_futuro": "6",
        "notas_accion": "Prueba automatizada NASA"
    }, follow_redirects=True)
    assert res_create.status_code == 200
    assert b"Prueba automatizada NASA" in res_create.data

    res_update = client.post("/editar/1", data={
        "estado_alerta": "CONTROLADO",
        "notas_accion": "Nota actualizada por test"
    }, follow_redirects=True)
    assert b"Nota actualizada por test" in res_update.data

    res_delete = client.post("/eliminar/1", follow_redirects=True)
    assert b"Registro eliminado de SQLite" in res_delete.data
