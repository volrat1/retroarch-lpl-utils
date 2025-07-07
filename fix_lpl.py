import sys
import requests
from bs4 import BeautifulSoup
import json
from rapidfuzz import process, fuzz
from urllib.parse import unquote
import re

# --- Utilidades ---

ROMAN_MAP = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
    7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII',
    13: 'XIII', 14: 'XIV', 15: 'XV', 16: 'XVI', 17: 'XVII', 18: 'XVIII', 19: 'XIX', 20: 'XX'
}

def arabic_to_roman(text):
    def replace(match):
        num = int(match.group())
        return ROMAN_MAP.get(num, match.group())
    return re.sub(r'\b([1-9]|1[0-9]|20)\b', replace, text)

def clean_label(label):
    return re.sub(r"[\(\[].*?[\)\]]", "", label).strip()

# --- Funciones principales ---

def get_names_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    names = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.png'):
            name = href[:-4]
            name = unquote(name)
            names.append(name)
    return names

def load_playlist(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_playlist(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main(playlist_path, url_index, threshold):
    thumbnail_names = get_names_from_url(url_index)
    thumbnail_lookup = {name.lower(): name for name in thumbnail_names}
    thumbnail_keys = list(thumbnail_lookup.keys())

    playlist = load_playlist(playlist_path)
    items = playlist.get('items', [])

    used_labels = set()
    accepted_matches = []  # (original, match, score)
    no_match = []          # (original, best_candidate, score)

    for item in items:
        original_label = item.get('label', '')
        if not original_label:
            continue

        cleaned_label = clean_label(original_label)
        search_variants = [cleaned_label]

        if re.search(r'\b[1-9]\b|\b1[0-9]\b|\b20\b', cleaned_label):
            roman_label = arabic_to_roman(cleaned_label)
            if roman_label != cleaned_label:
                search_variants.insert(0, roman_label)

        match_found = False
        for variant in search_variants:
            variant_lc = variant.lower()
            matches = process.extract(variant_lc, thumbnail_keys, scorer=fuzz.ratio, limit=5)

            for match_lc, score, _ in matches:
                best_match = thumbnail_lookup[match_lc]
                if score >= threshold and best_match not in used_labels:
                    item['label'] = best_match
                    used_labels.add(best_match)
                    accepted_matches.append((original_label, best_match, score))
                    print(f'Label "{original_label}" -> "{best_match}" (score {score})')
                    match_found = True
                    break

            if match_found:
                break

        if not match_found:
            best_try = matches[0] if matches else ("", 0, None)
            best_candidate_name = thumbnail_lookup.get(best_try[0], "?")
            no_match.append((original_label, best_candidate_name, best_try[1] if matches else 0))
            print(f'Label "{original_label}" no tuvo buen match aceptable')

    save_playlist(playlist, playlist_path.replace('.lpl', '_fixed.lpl'))

    if accepted_matches:
        print("\n=== Matches con menor score aceptado ===")
        for orig, match, score in sorted(accepted_matches, key=lambda x: x[2])[:20]:
            print(f'"{orig}" -> "{match}" (score {score})')

    if no_match:
        print("\n=== Casos sin match aceptable ===")
        for orig, best, score in no_match:
            print(f'"{orig}" (mejor candidato: "{best}", score {score})')

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python fix_labels.py playlist_path.lpl url_index [threshold]")
        sys.exit(1)

    playlist_path = sys.argv[1]
    url_index = sys.argv[2]
    threshold = int(sys.argv[3]) if len(sys.argv) == 4 else 70

    main(playlist_path, url_index, threshold)
