#!/usr/bin/env python3

import json
import csv
import sys

# Function to load the CSV and create a dictionary from filename -> label
def load_csv(csv_file):
    dictionary = {}
    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row['filename'].strip()
                label = row['label'].strip()
                dictionary[filename] = label
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' was not found.")
        sys.exit(1)
    return dictionary

# Function to load the .lpl file
def load_lpl(lpl_file):
    try:
        with open(lpl_file, mode='r', encoding='utf-8') as f:
            lpl_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The LPL file '{lpl_file}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The LPL file '{lpl_file}' is not a valid JSON.")
        sys.exit(1)
    return lpl_data

# Function to replace the labels in the items of the LPL file
def replace_labels(lpl_data, dictionary):
    for item in lpl_data.get("items", []):
        label = item.get("label")
        if label and label in dictionary:
            item["label"] = dictionary[label]
    return lpl_data

# Function to save the updated LPL file
def save_lpl(lpl_file, lpl_data):
    with open(lpl_file, mode='w', encoding='utf-8') as f:
        json.dump(lpl_data, f, ensure_ascii=False, indent=4)

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: ./replace_labels.py <csv_file> <lpl_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    lpl_file = sys.argv[2]

    # Load the CSV file and the LPL file
    dictionary = load_csv(csv_file)
    lpl_data = load_lpl(lpl_file)

    # Replace the labels in the LPL file
    updated_lpl_data = replace_labels(lpl_data, dictionary)

    # Save the updated LPL file
    save_lpl(lpl_file, updated_lpl_data)

    print(f"LPL file '{lpl_file}' updated with real game names.")

if __name__ == '__main__':
    main()
