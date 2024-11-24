import os
import sys
import shutil
import csv

def find_image(label, image_dir, extensions):
    """
    Searches for an image with the given name in the directory, testing various extensions.
    """
    for ext in extensions:
        image_path = os.path.join(image_dir, f"{label}.{ext}")
        if os.path.isfile(image_path):
            return image_path
    return None

def main(csv_file, images_dir):
    """
    Reads the CSV file and copies the images mentioned in the 'label' column to an output folder.
    """
    # Verify that the CSV file and the images directory exist
    if not os.path.isfile(csv_file):
        print(f"The CSV file '{csv_file}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(images_dir):
        print(f"The images directory '{images_dir}' does not exist.")
        sys.exit(1)

    output_dir = "copied_images"
    os.makedirs(output_dir, exist_ok=True)

    # Common image extensions
    extensions = ["png", "jpg", "jpeg", "gif", "bmp", "tiff"]

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if "label" not in reader.fieldnames:
            print("The CSV file does not contain a 'label' column.")
            sys.exit(1)

        for row in reader:
            label = row["label"]
            image_path = find_image(label, images_dir, extensions)
            if image_path:
                shutil.copy(image_path, output_dir)
                print(f"Copied: {image_path} -> {output_dir}")
            else:
                print(f"Warning: No image found for label '{label}'.")

    print(f"Copy complete. The images are located in '{output_dir}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 copy_images_from_csv.py <csv_file> <images_directory>")
        sys.exit(1)

    csv_file = sys.argv[1]
    images_dir = sys.argv[2]
    main(csv_file, images_dir)
