# Extract all .7z files in the current directory
# Use the -aoa option to overwrite duplicate files without asking for confirmation

# Extract .7z files with 7z and overwrite existing files
for file in *.7z; do
  7z x -aoa "$file"
done

# Extract .zip files with unzip and overwrite existing files
for file in *.zip; do
  unzip -o "$file"
done

# Extract .rar files with unrar and overwrite existing files
for file in *.rar; do
  unrar x -o+ "$file"
done

# Find all files inside subdirectories and move them to the current directory
# -mindepth 2 ensures that only files in subdirectories are considered (avoids the root directory)
# -type f selects only files, and -exec mv -t . '{}' + moves all found files to the current directory
find . -mindepth 2 -type f -exec mv -t . '{}' +

# Delete all empty subdirectories left after moving the files
# -type d selects directories, and -empty ensures that only empty directories are deleted
find . -type d -empty -delete

# Convert each .cue file in the current directory to a .chd file using chdman
# Use the base name of the .cue file for the output .chd file
for file in *.cue; do
  nice -n 2 taskset -c 0,11 chdman createcd -i "$file" -o "${file%.*}.chd"
done

for file in *.CUE; do
  nice -n 2 taskset -c 0,11 chdman createcd -i "$file" -o "${file%.*}.chd"
done

# Delete all files in the current directory except for .chd files
# -maxdepth 1 ensures that only files in the current directory are considered, not in subdirectories
# -type f selects only files, and ! -name "*.chd" excludes .chd files from deletion
find . -maxdepth 1 -type f ! -name "*.chd" -delete
