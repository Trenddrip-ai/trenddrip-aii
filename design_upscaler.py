# design_upscaler.py
from PIL import Image

def upscale_image(input_path):
    img = Image.open(input_path)
    img = img.resize((4500, 5400), Image.LANCZOS)
    img.save("upscaled_design.png")
    return "upscaled_design.png"
