# utils/image_handler.py

import os
import uuid
from werkzeug.utils import secure_filename

# FINAL: store images inside static/uploads/images
UPLOAD_FOLDER = os.path.join("static", "uploads", "images")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file):
    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()

    new_filename = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(UPLOAD_FOLDER, new_filename)
    file.save(filepath)

    return new_filename
