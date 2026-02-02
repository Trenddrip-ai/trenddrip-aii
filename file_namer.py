# file_namer.py
import re

def clean_filename(title):
    # remove illegal filename characters
    name = re.sub(r'[\\/*?:"<>|]', "", title)
    # shorten length
    name = name.strip()[:80]
    return name
