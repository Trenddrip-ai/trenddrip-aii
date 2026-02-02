# pod_formatter.py
from PIL import Image

def format_for_pod(input_path):
    canvas = Image.new("RGBA", (4500, 5400), (0, 0, 0, 0))
    design = Image.open(input_path)

    design.thumbnail((3800, 3800), Image.LANCZOS)

    x = (4500 - design.width) // 2
    y = (5400 - design.height) // 2

    canvas.paste(design, (x, y), design)
    canvas.save("final_pod_design.png")

    return "final_pod_design.png"
