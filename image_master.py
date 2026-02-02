import base64
import os
from openai import OpenAI
import cloudinary
import cloudinary.uploader
from PIL import Image

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cloudinary config from environment
cloudinary.config(secure=True)


def make_pod_ready(input_path):
    """
    Converts transparent PNG to 4500x5400 @300 DPI for POD printing
    """
    output_path = input_path.replace(".png", "_POD.png")

    img = Image.open(input_path).convert("RGBA")

    # Create POD canvas
    pod_canvas = Image.new("RGBA", (4500, 5400), (0, 0, 0, 0))

    # Resize design to fit shirt nicely
    img.thumbnail((3800, 4800), Image.LANCZOS)

    # Center the design
    x = (4500 - img.width) // 2
    y = (5400 - img.height) // 2

    pod_canvas.paste(img, (x, y), img)

    pod_canvas.save(output_path, dpi=(300, 300))

    print("✅ POD image created:", output_path)
    return output_path


def upload_to_cloudinary(file_path):
    """
    Uploads image to Cloudinary and returns the URL
    """
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]


def generate_image(prompt):
    """
    Generates image with OpenAI → makes POD ready → uploads → returns URL
    """

    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", "design.png")

    print("🎨 Generating image...")

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536",          # Correct supported size
        background="transparent"
    )

    import base64

def generate_image(prompt):
    """
    Generates image with OpenAI → makes POD ready → uploads → returns URL
    """

    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", "design.png")

    print("🎨 Generating image...")

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536",
        background="transparent"
    )

    image_base64 = result.data[0].b64_json

    # ✅ Proper base64 decode (THIS FIXES EVERYTHING)
    image_bytes = base64.b64decode(image_base64)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print("✅ Image saved locally:", output_path)

    # Convert to POD
    pod_ready_path = make_pod_ready(output_path)

    # Upload
    image_url = upload_to_cloudinary(pod_ready_path)

    print("☁️ Uploaded to Cloudinary:", image_url)

    return image_url



