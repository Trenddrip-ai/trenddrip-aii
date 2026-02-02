# trend_engine.py
import random

GRAFFITI_MASCOTS = [
    "graffiti style cartoon monkey mascot holding spray can",
    "retro raccoon street artist mascot",
    "cute fox graffiti mascot with hoodie",
    "urban panda mascot logo",
    "street bear mascot in hoodie"
]

TYPOGRAPHY = [
    "bold graffiti word art saying STREET CULTURE",
    "retro street typography saying NO RULES",
    "urban graffiti text saying STAY WILD",
    "street slogan art saying CREATE CHAOS",
    "minimal bold text logo saying FUTURE VIBES"
]

ANIME = [
    "anime style street hero character with hoodie",
    "anime street ninja mascot",
    "anime cyber street warrior",
    "anime urban explorer character",
    "anime hoodie graffiti character"
]

LOGOS = [
    "minimalist streetwear emblem logo with symbols",
    "urban circular logo emblem",
    "badge style street logo design",
    "clean iconic street brand logo",
    "sticker style streetwear emblem"
]

def build_prompt(style_choice):
    if style_choice == "1":
        subject = random.choice(GRAFFITI_MASCOTS)
    elif style_choice == "2":
        subject = random.choice(TYPOGRAPHY)
    elif style_choice == "3":
        subject = random.choice(ANIME)
    else:
        subject = random.choice(LOGOS)

    return f"""
Create a clean, high-detail VECTOR illustration for a streetwear t-shirt.

Subject: {subject}

Design rules:
- Bold thick outlines
- 3-5 color palette
- Center composition
- Sticker/logo style
- Transparent background
- Professional POD design
"""
