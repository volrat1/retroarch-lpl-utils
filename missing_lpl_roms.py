import os
import sys
import json

def read_playlist(playlist_file):
    """Reads the JSON playlist file and extracts the ROM filenames."""
    playlist_files = set()

    try:
        with open(playlist_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data.get("items", []):
                if "path" in item:
                    file_name = os.path.basename(item["path"])  # Gets the filename
                    playlist_files.add(file_name.lower())  # Normalize to lowercase
    except Exception as e:
        print(f"Error reading the playlist file: {e}")
    
    return playlist_files

def search_rom_files(roms_directory, extensions):
    """Searches for files in the ROM directory that match the given extensions."""
    rom_files = []

    for root, _, files in os.walk(roms_directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                rom_files.append(os.path.basename(file).lower())  # Normalize to lowercase
    
    return rom_files

def main():
    if len(sys.argv) < 4:
        print("Usage: python check_roms.py <playlist_file.lpl> <roms_directory> <extension1> [<extension2> ...]")
        sys.exit(1)

    playlist_file = sys.argv[1]
    roms_directory = sys.argv[2]
    extensions = [ext.lower() for ext in sys.argv[3:]]

    # Read files from the playlist
    playlist_files = read_playlist(playlist_file)
    print(f"Playlist files: {len(playlist_files)} found.")

    # Search files in the ROM directory
    rom_files = search_rom_files(roms_directory, extensions)
    print(f"ROM files in directory: {len(rom_files)} found.")

    # Find files that are not in the playlist
    missing_files = sorted(set(rom_files) - playlist_files)

    # Generate output file
    output_file = "missing_roms.txt"
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for file in missing_files:
            out_file.write(f"{file}\n")

    print(f"{len(missing_files)} files that are not in the playlist have been listed.")
    print(f"Output file generated: {output_file}")

if __name__ == "__main__":
    main()
