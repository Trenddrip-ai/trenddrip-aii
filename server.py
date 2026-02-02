from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess
import glob
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class RequestData(BaseModel):
    style: int
    count: int

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate(data: RequestData):
    subprocess.run(
        ["python", "auto_runner.py"],
        input=f"{data.style}\n{data.count}\n",
        text=True
    )

    files = glob.glob("TrendDrip_Collection_*.zip")
    latest = max(files, key=os.path.getctime)

    return {"zip": latest}

@app.get("/download")
def download(zip_name: str):
    return FileResponse(zip_name, media_type='application/zip', filename=zip_name)
