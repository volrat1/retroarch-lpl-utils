#!/bin/bash

# Folder where the compressed files are located
ORIGIN="${1:-.}"

# Output folder
DESTINATION="${2:-./descomprimidos}"

# Create output folder if it doesn't exist
mkdir -p "$DESTINATION"

# Loop through all files in the origin folder
for file in "$ORIGIN"/*; do
  case "$file" in
    *.zip)
      echo "Extracting ZIP: $file"
      unzip -o "$file" -d "$DESTINATION"
      ;;
    *.rar)
      echo "Extracting RAR: $file"
      unrar x -o+ "$file" "$DESTINATION"
      ;;
    *.7z)
      echo "Extracting 7z: $file"
      7z x -y -o"$DESTINATION" "$file"
      ;;
    *)
      echo "Ignoring: $file"
      ;;
  esac
done

echo "All files have been processed."
