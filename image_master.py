# image_master.py
from openai import OpenAI
import base64

client = OpenAI()

def generate_image(prompt):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        background="transparent"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open("raw_design.png", "wb") as f:
        f.write(image_bytes)

    return "raw_design.png"

