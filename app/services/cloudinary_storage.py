import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dusxsqs57",     # YOUR cloud name
    api_key="873249384976328",
    api_secret="Xc1YBPTXmvXKpEfxSbkaJwaASywT"
)

def upload_to_cloudinary(image_path):
    result = cloudinary.uploader.upload(
        image_path,
        folder="campa_stock"
    )
    return result["secure_url"]