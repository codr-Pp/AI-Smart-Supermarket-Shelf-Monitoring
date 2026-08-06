from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

BUCKET_NAME = "campa-stock-images"

def upload_image(file_path, object_name):
    client.fput_object(
        BUCKET_NAME,
        object_name,
        file_path
    )