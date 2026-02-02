import os
import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO

import cloudinary
import cloudinary.uploader

# ---------- Cloudinary Config ----------
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

def upload_image(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]


# ---------- OpenAI Client ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image(prompt):
    print("\n🎨 Generating image with prompt:\n", prompt)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        background="transparent"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_bytes))

    # Temporary save
    if not os.path.exists("temp"):
        os.makedirs("temp")

    path = f"temp/design.png"
    image.save(path)

    # Upload to Cloudinary
    url = upload_image(path)
    print("✅ Image URL:", url)

    return url


