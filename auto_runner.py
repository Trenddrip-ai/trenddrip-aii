from trend_engine import build_prompt
from prompt_evolver import evolve_prompt
from image_master import generate_image
from design_upscaler import upscale_image
from pod_formatter import format_for_pod
from listing_writer import create_listing
from file_namer import clean_filename
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("""
🚀 TrendDrip Super Machine Running...

Choose your design style:
1 - Graffiti Mascots
2 - Street Typography
3 - Anime Streetwear
4 - Logo Emblems
""")

style = input("Enter choice (1-4): ")
count = int(input("How many designs do you want to generate? "))

style_names = {
    "1": "Graffiti_Mascots",
    "2": "Street_Typography",
    "3": "Anime_Streetwear",
    "4": "Logo_Emblems"
}

date_stamp = datetime.now().strftime("%Y-%m-%d")
collection_folder = f"{style_names.get(style, 'Collection')}_{date_stamp}"

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", collection_folder)
os.makedirs(OUTPUT_DIR, exist_ok=True)

for i in range(count):
    print(f"\n--- Design {i+1} ---")

    prompt = build_prompt(style)
    smart_prompt = evolve_prompt(prompt)

    raw = generate_image(smart_prompt)
    upscaled = upscale_image(raw)
    final = format_for_pod(upscaled)

    listing = create_listing(smart_prompt)

    # Extract title
    lines = listing.split("\n")
    title = ""
    for line in lines:
        if "title" in line.lower():
            continue
        if line.strip() and len(line) > 10:
            title = line.strip()
            break

    safe_name = clean_filename(title)

    img_path = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
    txt_path = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")

    if os.path.exists(img_path):
        os.remove(img_path)
    if os.path.exists(txt_path):
        os.remove(txt_path)

    shutil.move(final, img_path)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(listing)

print(f"\n✅ Designs saved in: {OUTPUT_DIR}\n")
