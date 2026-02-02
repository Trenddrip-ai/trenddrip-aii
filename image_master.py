import base64
import os
import uuid
import cloudinary
import cloudinary.uploader
from openai import OpenAI

client = OpenAI()

# Cloudinary config from Render / local env
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt):
    print("🎨 Generating image...")

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json

    # -------- Save locally FIRST --------
    filename = f"{uuid.uuid4()}.png"
    local_path = os.path.join(OUTPUT_DIR, filename)

    with open(local_path, "wb") as f:
        f.write(base64.b64decode(image_base64))

    print("💾 Saved locally:", local_path)

    # -------- Upload to Cloudinary --------
    upload = cloudinary.uploader.upload(local_path)
    image_url = upload["secure_url"]

    print("☁️ Uploaded:", image_url)

    return local_path, image_url


