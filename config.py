"""Runtime configuration for the Flask application.

Values default to the original local settings so the existing workflow keeps
running. Override them with environment variables before publishing or
deploying the project.
"""

import os


class Config:
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")
    MODEL_PATH = os.getenv("MODEL_PATH", "runs/detect/train/weights/best.pt")

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "duwsxq5n7")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "873249384976328")
    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET",
        "Xc1YBPTXmvXKpEfxSbkaJwaASyw",
    )

    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_FROM = os.getenv("EMAIL_FROM", "campavision.ai@gmail.com")
    EMAIL_TO = os.getenv("EMAIL_TO", "project02campa@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "xvkfwzucmfiupjkt")
