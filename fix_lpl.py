# Requires a venv with requests, beautifulsoup4, and rapidfuzz installed
# python3 -m venv venv
# source venv/bin/activate
# pip install requests beautifulsoup4 rapidfuzz

import sys
import requests
from bs4 import BeautifulSoup
import json
from rapidfuzz import process, fuzz
from urllib.parse import unquote
import re

def get_names_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    names = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.png'):
            name = href[:-4]  # remove ".png"
            name = unquote(name)  # decode %20, etc.
            names.append(name)
    return names

def load_playlist(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_playlist(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_label(label):
    # Remove content inside parentheses or brackets, including the parentheses/brackets
    return re.sub(r"[\(\[].*?[\)\]]", "", label).strip()

def main(playlist_path, url_index, threshold):
    thumbnail_names = get_names_from_url(url_index)

    # Crear diccionario original → lowercased, para mapear luego al nombre exacto
    thumbnail_lookup = {name.lower(): name for name in thumbnail_names}
    thumbnail_keys = list(thumbnail_lookup.keys())

    playlist = load_playlist(playlist_path)
    items = playlist.get('items', [])

    for item in items:
        original_label = item.get('label', '')
        if not original_label:
            continue

        cleaned_label = clean_label(original_label).lower()

        best_key, score, _ = process.extractOne(cleaned_label, thumbnail_keys, scorer=fuzz.ratio)
        if score >= threshold:
            best_match = thumbnail_lookup[best_key]
            item['label'] = best_match
            print(f'Label "{original_label}" -> "{best_match}" (score {score})')
        else:
            print(f'Label "{original_label}" had no good match (best: "{thumbnail_lookup[best_key]}" score {score})')

    save_playlist(playlist, playlist_path.replace('.lpl', '_fixed.lpl'))

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python fix_labels.py playlist_path.lpl url_index [threshold]")
        sys.exit(1)

    playlist_path = sys.argv[1]
    url_index = sys.argv[2]
    threshold = int(sys.argv[3]) if len(sys.argv) == 4 else 70

    main(playlist_path, url_index, threshold)
