import os
import shutil
from datetime import datetime

from trend_engine import build_prompt
from prompt_evolver import evolve_prompt
from image_master import generate_image
from listing_writer import create_listing
from file_namer import clean_filename


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_ROOT = os.path.join(BASE_DIR, "outputs")


def run_collection(style_name: str, count: int):
    print(f"\n🚀 Generating {count} designs for: {style_name}\n")

    date_stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    collection_folder = os.path.join(
        OUTPUT_ROOT, f"{style_name}_{date_stamp}"
    )

    os.makedirs(collection_folder, exist_ok=True)

    for i in range(1, count + 1):
        print(f"\n--- Design {i} ---\n")

        prompt = build_prompt(style_name)
        smart_prompt = evolve_prompt(prompt)

        image_url = generate_image(smart_prompt)
        print("Image URL:", image_url)

        listing = create_listing(smart_prompt)

        lines = listing.split("\n")
        title = "Streetwear Design"
        for line in lines:
            if line.strip() and len(line) > 10:
                title = line.strip()
                break

        safe_name = clean_filename(title)

        txt_path = os.path.join(collection_folder, f"{safe_name}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(listing)
            f.write("\n\nIMAGE URL:\n")
            f.write(image_url)

        print(f"✅ Saved: {txt_path}")

    zip_name = f"TrendDrip_Collection_{date_stamp}"
    zip_path = os.path.join(BASE_DIR, zip_name)

    shutil.make_archive(
        zip_path,
        'zip',
        collection_folder
    )

    print(f"\n📦 Zipped at: {zip_path}.zip\n")
    return f"{zip_path}.zip"


if __name__ == "__main__":
    print("""
🎨 TrendDrip Super Machine

1 - Graffiti Mascots
2 - Street Typography
3 - Anime Streetwear
4 - Logo Emblems
""")

    style_choice = input("Enter choice (1-4): ")
    count = int(input("How many designs? "))

    style_map = {
        "1": "Graffiti_Mascots",
        "2": "Street_Typography",
        "3": "Anime_Streetwear",
        "4": "Logo_Emblems"
    }

    style_name = style_map.get(style_choice, "Graffiti_Mascots")

    zip_file = run_collection(style_name, count)
    print(f"\n🔥 DONE. Zip ready:\n{zip_file}\n")



        

