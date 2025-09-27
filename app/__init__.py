# File: app/__init__.py

from flask import Flask, render_template, request, redirect, flash
import os
import pandas as pd

# allowed files
ALLOWED_EXTENSIONS = {'csv' , 'xlsx'}

# check that the name of the file is valid
def is_valid_file_name(filename):
    # if there is not . then not valid
    if '.' not in filename:
        return False
    
    # if the most right . split is not csv or xlsx
    if filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return False

    return True

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev"  # Override in production

    # create folder for uploads
    UPLOAD_FOLDER = 'app/static/uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    @app.route("/")
    def index():
        return "Student Finance Dashboard is running 🚀"
    
    @app.route("/test")
    def test():
        return {"status": "ok", "message": "Test route working!"}
    

    @app.route("/upload", methods=["GET", "POST"])
    def upload():
        if request.method == "POST":
            # Incomplete form submitted
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            
            file = request.files["file"]

            # No file selected
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            
            # check valid extension
            if file and is_valid_file_name(file.filename):
                try:
                    # Extract extension
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    # read file
                    if ext == "csv":
                        df = pd.read_csv(file)
                    else:
                        file.seek(0)
                        df = pd.read_excel(file, engine="openpyxl")
                    
                    # Basic check: must have at least 2 expected columns
                    if not {"Date", "Description", "Amount"}.issubset(df.columns):
                        flash("Invalid file format — required columns: Date, Description, Amount")
                        return redirect(request.url)

                    preview = df.head(5).to_html(classes='table table-striped', index=False)
                    return render_template("upload.html", table_preview=preview)

                except Exception as e:
                    flash(f"Error reading file: {str(e)}")
                    return redirect(request.url)

            else:
                flash("Invalid file type. Only .csv and .xlsx are allowed.")
                return redirect(request.url)

        return render_template("upload.html", table_preview=None)

    return app

