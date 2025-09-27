# File: tests/test_upload_route.py

import io
from tests.conftest import make_csv_bytes, make_excel_bytes

def test_upload_get_renders_form(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Upload Statement File" in resp.data

def test_upload_post_no_file_part(client):
    resp = client.post("/upload", data={}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"No file part" in resp.data

def test_upload_post_empty_filename(client):
    data = {"file": (io.BytesIO(b""), "")}
    resp = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert b"No selected file" in resp.data

def test_upload_post_invalid_extension(client):
    data = {"file": (io.BytesIO(b"hello"), "bad.pdf")}
    resp = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert b"Invalid file type. Only .csv and .xlsx are allowed." in resp.data

def test_upload_post_missing_columns_csv(client):
    # Missing "Amount" column on purpose
    bad_csv = io.BytesIO(b"Date,Description\n2025-01-01,Coffee\n")
    data = {"file": (bad_csv, "bad.csv")}
    resp = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert b"Invalid file format" in resp.data

def test_upload_post_valid_csv_shows_preview(client):
    csv_bytes = make_csv_bytes([
        ("2025-01-01", "Coffee", -12.5),
        ("2025-01-02", "Salary", 5000),
    ])
    data = {"file": (csv_bytes, "ok.csv")}
    resp = client.post("/upload", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    # Table preview present
    assert b"Preview" in resp.data
    assert b"Coffee" in resp.data
    assert b"Salary" in resp.data

def test_upload_post_valid_excel_shows_preview(client):
    xlsx_bytes = make_excel_bytes([
        ("2025-01-03", "Groceries", -120.0),
        ("2025-01-04", "Gift", -80.0),
    ])
    data = {"file": (xlsx_bytes, "ok.xlsx")}
    resp = client.post("/upload", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert b"Preview" in resp.data
    assert b"Groceries" in resp.data