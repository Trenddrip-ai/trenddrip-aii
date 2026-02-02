import os
import zipfile
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from .image_master import generate_image

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


class GenerateRequest(BaseModel):
    style: int
    count: int


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
def generate(req: GenerateRequest):
    images = []

    for i in range(req.count):
        img = generate_image(req.style, i)
        images.append(img)

    zip_name = "TrendDrip_Collection.zip"
    zip_path = os.path.join("outputs", zip_name)

    with zipfile.ZipFile(zip_path, "w") as z:
        for img in images:
            z.write(img, os.path.basename(img))

    return {"images": images, "zip": zip_name}


@app.get("/outputs/{file}")
def get_image(file: str):
    return FileResponse(f"outputs/{file}")


@app.get("/download/{zip_name}")
def download(zip_name: str):
    return FileResponse(f"outputs/{zip_name}", media_type="application/zip")
