import os
from fastapi import FastAPI
from pydantic import BaseModel

from image_master import generate_image
from pod import make_pod_ready
from zipper import zip_collection

app = FastAPI(title="TrendDrip AI API")


class GenerateRequest(BaseModel):
    style: int
    count: int


STYLE_MAP = {
    1: "Graffiti_Mascots",
    2: "Street_Typography",
    3: "Anime_Streetwear",
    4: "Logo_Emblems",
}


@app.post("/generate")
def generate_collection(req: GenerateRequest):
    style_name = STYLE_MAP.get(req.style, "Graffiti_Mascots")

    base_output = os.path.join("outputs", f"{style_name}")
    os.makedirs(base_output, exist_ok=True)

    for i in range(req.count):
        print(f"Generating design {i+1}...")

        # 1. Generate raw image
        raw_path = generate_image(style_name)

        # 2. Make POD ready (transparent, 4500x5400)
        pod_path = make_pod_ready(raw_path)

        # Move into collection folder
        final_path = os.path.join(base_output, f"design_{i+1}.png")
        os.replace(pod_path, final_path)

    # 3. Zip entire folder
    zip_name = zip_collection(base_output)

    return {"zip": zip_name}
