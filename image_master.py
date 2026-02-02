import base64
import os
from openai import OpenAI
import cloudinary
import cloudinary.uploader

client = OpenAI()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt: str) -> str:
    print("🎨 Generating image...")

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        background="transparent"
    )

    image_base64 = result.data[0].b64_json

    # Save locally FIRST
    file_path = os.path.join(OUTPUT_DIR, "design.png")
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(image_base64))

    print("✅ Image saved locally:", file_path)

    # Upload to Cloudinary SECOND
    upload = cloudinary.uploader.upload(file_path)
    image_url = upload["secure_url"]

    print("☁️ Uploaded to Cloudinary:", image_url)

    return file_path  # <-- THIS IS CRITICAL


