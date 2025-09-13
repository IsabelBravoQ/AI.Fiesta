import pytest

@pytest.fixture()
def client(monkeypatch):
    import app as app_module  


    monkeypatch.setattr(app_module, "llm", lambda *a, **k: {
        "tema": a[0] if a else "Tema",
        "música": ["A", "B"],
        "decoración": ["X"],
        "juegos": ["Y"],
        "comida": ["Z"],
        "bebidas": ["W"]
    })
    monkeypatch.setattr(app_module, "bbdd", lambda *a, **k: "ok")

    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200

def test_fiestas_ok(client):
    payload = {
        "p_tema": "Piratas",
        "edad_invitados": "Adultos",
        "numero_invitados": 10,
        "presupuesto": "Alto",
        "lugar": "finca"
    }
    r = client.post("/fiestas", json=payload)
    assert r.status_code == 200
    data = r.get_json()

    key = "plan" if "plan" in data else "fiesta"
    assert key in data
    for k in ["música","decoración","juegos","comida","bebidas"]:
        assert k in data[key]

def test_fiestas_400(client):
    # Falta 'lugar'
    r = client.post("/fiestas", json={
        "p_tema": "Halloween",
        "edad_invitados": "Adolescentes",
        "numero_invitados": 8,
        "presupuesto": "Bajo"
    })
    assert r.status_code == 400