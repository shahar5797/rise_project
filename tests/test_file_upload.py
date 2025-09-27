# File: tests/test_file_upload.py

from app import is_valid_file_name
import io

def test_is_valid_file_name_good_csv():
    assert is_valid_file_name("statement.csv") is True

def test_is_valid_file_name_good_xlsx():
    assert is_valid_file_name("report.XLSX") is True  

def test_is_valid_file_name_bad_ext():
    assert is_valid_file_name("notes.pdf") is False

def test_is_valid_file_name_no_dot():
    assert is_valid_file_name("mystatement") is False

def test_upload_post_fake_csv_parsing_error(client):
    # Bytes that are invalid UTF-8 → pandas.read_csv should raise a UnicodeDecodeError
    bad_bytes = io.BytesIO(b"\xff\xfe\xfa\xfb")
    data = {"file": (bad_bytes, "evil.csv")}
    resp = client.post("/upload", data=data,
                       content_type="multipart/form-data",
                       follow_redirects=True)
    assert resp.status_code == 200
    assert b"Error reading file" in resp.data  # from your flash in the outer try/except


def test_upload_post_fake_excel_parsing_error(client):
    # Not a valid XLSX (xlsx is a zip file) → pandas/openpyxl should raise (e.g., BadZipFile)
    bad_bytes = io.BytesIO(b"this is not a real xlsx zip file")
    data = {"file": (bad_bytes, "evil.xlsx")}
    resp = client.post("/upload", data=data,
                       content_type="multipart/form-data",
                       follow_redirects=True)
    assert resp.status_code == 200
    assert b"Error reading file" in resp.data