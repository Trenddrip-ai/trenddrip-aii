import base64
import os
import cloudinary
import cloudinary.uploader
from openai import OpenAI
from datetime import datetime

client = OpenAI()

# ---------- Cloudinary ----------
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

# ---------- Folders ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def upload_image(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]


def generate_image(prompt):
    print("🎨 Generating image...")

    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_bytes = img.data[0].b64_json
    file_name = f"design_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    local_path = os.path.join(OUTPUT_DIR, file_name)

    # ✅ SAVE LOCALLY (this fixes empty folders)
    with open(local_path, "wb") as f:
        f.write(base64.b64decode(image_bytes))

    print("💾 Saved locally:", local_path)

    # ✅ Upload to Cloudinary
    url = upload_image(local_path)
    print("☁️ Cloudinary URL:", url)

    return local_path, url

