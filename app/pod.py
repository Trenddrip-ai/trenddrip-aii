from PIL import Image

def make_pod_ready(input_path: str) -> str:
    img = Image.open(input_path).convert("RGBA")

    canvas = Image.new("RGBA", (4500, 5400), (0, 0, 0, 0))
    img.thumbnail((3800, 5000))

    x = (4500 - img.width) // 2
    y = (5400 - img.height) // 2

    canvas.paste(img, (x, y), img)

    output_path = input_path.replace(".png", "_POD.png")
    canvas.save(output_path)

    return output_path
