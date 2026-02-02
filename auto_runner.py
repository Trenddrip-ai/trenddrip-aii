import os
from datetime import datetime

from trend_engine import build_prompt
from prompt_evolver import evolve_prompt
from listing_writer import create_listing
from file_namer import clean_filename
from image_master import generate_image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_trenddrip(style, count):
    print("\n🚀 TrendDrip Super Machine Running...\n")

    style_names = {
        "1": "Graffiti_Mascots",
        "2": "Street_Typography",
        "3": "Anime_Streetwear",
        "4": "Logo_Emblems"
    }

    style_folder = style_names.get(style, "Graffiti_Mascots")
    dated_folder = f"{style_folder}_{datetime.now().strftime('%Y-%m-%d')}"
    full_output_path = os.path.join(OUTPUT_DIR, dated_folder)
    os.makedirs(full_output_path, exist_ok=True)

    results = []

    for i in range(count):
        print(f"\n🎨 --- Design {i+1} ---\n")

        # ---------- Prompt ----------
        prompt = build_prompt(style_folder)
        smart_prompt = evolve_prompt(prompt)

        # ---------- Listing ----------
        listing = create_listing(smart_prompt)

        # Extract title from listing
        lines = listing.split("\n")
        title = "Streetwear Design"

        for line in lines:
            if "title" in line.lower():
                continue
            if line.strip() and len(line) > 10:
                title = line.strip()
                break

        safe_name = clean_filename(title)

        # ---------- Image Generation ----------
        local_path, image_url = generate_image(smart_prompt)

        # Move image into this design folder
        final_img_path = os.path.join(full_output_path, f"{safe_name}.png")
        os.rename(local_path, final_img_path)

        # ---------- Save TXT ----------
        txt_path = os.path.join(full_output_path, f"{safe_name}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(listing)

        print("✅ Saved:", final_img_path)
        print("☁️ URL:", image_url)

        results.append({
            "title": title,
            "image_url": image_url,
            "local_path": final_img_path,
            "listing": listing
        })

    print(f"\n✅ Designs saved in: {full_output_path}\n")
    return results



