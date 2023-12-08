import os
import json
import argparse
import fnmatch
import colorsys
import random
from os.path import splitext, exists, join

def find_common_prefix(strings):
    if not strings:
        return ""
    s1 = min(strings)
    s2 = max(strings)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7 + 0.3 * (i % 2)  # Alternate between 70% and 100% saturation
        lightness = 0.5
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append({"r": r, "g": g, "b": b})
    random.shuffle(colors)  # Shuffle the colors to get a pseudo-random order
    return colors

def generate_json(directory):
    filenames = [f for f in os.listdir(directory) if fnmatch.fnmatch(f, '*.ply') or 
                fnmatch.fnmatch(f, '*.glb') or fnmatch.fnmatch(f, '*.stl') or fnmatch.fnmatch(f, '*.fbx')]
    common_prefix = find_common_prefix(filenames)

    # Debugging: Print the number of filenames found
    print(f"Number of files found: {len(filenames)}")

    distinct_colors = generate_distinct_colors(128)

    data = []
    for filename in filenames:
        name_without_extension = splitext(filename)[0]
        cleaned_name = name_without_extension.replace(common_prefix, '', 1).replace('_', ' ')
        color = distinct_colors.pop(0)  # Get the next color in the shuffled list

        segment = {
            "label": cleaned_name,
            "filename": filename,
            "color": {
                "r": color["r"],
                "g": color["g"],
                "b": color["b"],
                "a": 0.8  # Fixed transparency value
            }
        }
        data.append(segment)

    # Sorting the data based on label
    data.sort(key=lambda x: x['label'])

    output_file = join(directory, 'model_meta.json')

    # Check if the output file already exists and delete it if it does
    if exists(output_file):
        os.remove(output_file)
    
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Generate a model metadata JSON file in the specified directory.")
    parser.add_argument('--path', type=str, required=True, help='The directory path where the JSON file will be created and containing the files.')

    args = parser.parse_args()

    generate_json(args.path)

if __name__ == "__main__":
    main()
