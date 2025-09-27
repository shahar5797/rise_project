# File: tests/conftest.py

import io
import pandas as pd
import pytest

from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # not using WTForms but keeping future-proof
    )
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# generate a fake csv for testing
def make_csv_bytes(rows, columns=("Date","Description","Amount")):
    import csv
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    writer.writerows(rows)
    return io.BytesIO(buf.getvalue().encode("utf-8"))

# generate a fake excel for testing
def make_excel_bytes(rows, columns=("Date","Description","Amount")):
    buf = io.BytesIO()
    df = pd.DataFrame(rows, columns=list(columns))
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    buf.seek(0)
    return buf