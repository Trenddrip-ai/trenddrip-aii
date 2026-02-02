from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
import subprocess
import os
import zipfile
from datetime import datetime

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

HTML_PAGE = """
<html>
<head>
    <title>TrendDrip AI</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:50px;">
    <h1>🚀 TrendDrip AI Generator</h1>

    <form method="post">
        <label>Choose Style:</label><br><br>
        <select name="style">
            <option value="1">Graffiti Mascots</option>
            <option value="2">Street Typography</option>
            <option value="3">Anime Streetwear</option>
            <option value="4">Logo Emblems</option>
        </select><br><br>

        <label>Number of Designs:</label><br><br>
        <input type="number" name="count" value="10"/><br><br>

        <button type="submit">Generate Designs</button>
    </form>
</body>
</html>
"""

def zip_latest_collection():
    folders = [os.path.join(OUTPUTS_DIR, f) for f in os.listdir(OUTPUTS_DIR)]
    latest_folder = max(folders, key=os.path.getmtime)

    zip_name = f"TrendDrip_Collection_{datetime.now().strftime('%H%M%S')}.zip"
    zip_path = os.path.join(BASE_DIR, zip_name)

    with zipfile.ZipFile(zip_path, 'w') as z:
        for root, _, files in os.walk(latest_folder):
            for file in files:
                full_path = os.path.join(root, file)
                z.write(full_path, file)

    return zip_path

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/", response_class=FileResponse)
def run_trenddrip(style: str = Form(...), count: int = Form(...)):
    subprocess.run(
        ["python", "auto_runner.py"],
        input=f"{style}\n{count}\n",
        text=True
    )

    zip_path = zip_latest_collection()
    return FileResponse(zip_path, filename=os.path.basename(zip_path))


