import os
import sys
import csv
from difflib import SequenceMatcher

def clean_name(name):
    """Cleans the filename by removing text in parentheses and the file extension."""
    name = os.path.splitext(name)[0]  # Removes the extension
    name = ''.join(part.split('(')[0] for part in name.split(')'))  # Removes content in parentheses
    return name.strip()

def find_best_match(rom_name, thumbs):
    """Finds the best match for a ROM name among the thumbnails."""
    best_match = None
    best_ratio = 0
    for thumb in thumbs:
        thumb_clean = clean_name(thumb)
        match_ratio = SequenceMatcher(None, rom_name, thumb_clean).ratio()
        if match_ratio > best_ratio:
            best_match = thumb
            best_ratio = match_ratio
    return best_match

def main(roms_dir, thumbs_dir):
    """Reads files from both directories and generates a CSV file with the best matches."""
    if not os.path.isdir(roms_dir) or not os.path.isdir(thumbs_dir):
        print("Both arguments must be valid directories.")
        sys.exit(1)

    roms = sorted(os.listdir(roms_dir))
    thumbs = sorted(os.listdir(thumbs_dir))

    matches = []
    for rom in roms:
        rom_clean = clean_name(rom)
        best_match = find_best_match(rom_clean, thumbs)
        if best_match:
            rom_no_ext = os.path.splitext(rom)[0]  # Remove the extension from the ROM
            best_match_no_ext = os.path.splitext(best_match)[0]  # Remove the extension from the thumbnail
            matches.append((rom_no_ext, best_match_no_ext))

    output_file = "rom_thumbnail_matches.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "label"])
        writer.writerows(matches)

    print(f"CSV file generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 match_names.py <roms_directory> <thumbs_directory>")
        sys.exit(1)

    roms_dir = sys.argv[1]
    thumbs_dir = sys.argv[2]
    main(roms_dir, thumbs_dir)
