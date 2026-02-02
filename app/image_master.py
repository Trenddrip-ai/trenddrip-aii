import os
import base64
from openai import OpenAI
from .pod import make_pod_ready

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(style: int) -> str:
    styles = {
        1: "graffiti cartoon mascot, bold vector, sticker style, tshirt graphic, no background",
        2: "street typography lettering, bold vector, tshirt graphic, no background",
        3: "anime streetwear character, cel shaded, tshirt graphic, no background",
        4: "logo emblem symbol, minimalist vector, tshirt graphic, no background",
        5: "cyberpunk skull neon vector, tshirt graphic, no background",
        6: "retro 90s cartoon character vector, tshirt graphic, no background",
    }
    return styles.get(style, styles[1])


def generate_image(style: int, index: int) -> str:
    prompt = build_prompt(style)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        background="transparent"
    )

    image_bytes = base64.b64decode(result.data[0].b64_json)

    os.makedirs("outputs", exist_ok=True)
    raw_path = f"outputs/design_{index}.png"

    with open(raw_path, "wb") as f:
        f.write(image_bytes)

    return make_pod_ready(raw_path)
