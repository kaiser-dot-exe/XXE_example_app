import io, re, pathlib
import pytest
from app import app

@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client

def upload_xml(client, content: bytes, name="test.xml"):
    data = {"xmlfile": (io.BytesIO(content), name)}
    return client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)

def test_benign_ok(client):
    benign = pathlib.Path("samples/benign.xml").read_bytes()
    resp = upload_xml(client, benign, "benign.xml")
    assert resp.status_code == 200
    assert b"Parse Ba&#351;ar&#305;l&#305;" in resp.data or b"Parse Başarılı" in resp.data

def test_xxe_doctype_blocked(client):
    xxe = pathlib.Path("samples/xxe_attempt_doctype.xml").read_bytes()
    resp = upload_xml(client, xxe, "xxe_doctype.xml")
    assert resp.status_code == 200
    assert b"DTD/ENTITY alg&#305;land&#305;" in resp.data or b"DTD/ENTITY algılandı" in resp.data

def test_xxe_parameter_entity_blocked(client):
    xxe = pathlib.Path("samples/xxe_attempt_parameter_entity.xml").read_bytes()
    resp = upload_xml(client, xxe, "xxe_param.xml")
    assert resp.status_code == 200
    assert b"reddedildi" in resp.data  # flash mesajı
