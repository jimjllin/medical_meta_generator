import os
import json
import argparse
import fnmatch
import colorsys
import random
from os.path import splitext, exists, join

def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7 + 0.3 * (i % 2)  # 輪流選擇70%和100%的飽和度
        lightness = 0.5
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append({"r": r, "g": g, "b": b})
    random.shuffle(colors)  # 打亂顏色順序以獲得偽隨機順序
    return colors

def find_common_prefix(strings):
    if not strings:
        return ""
    s1 = min(strings)
    s2 = max(strings)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

def read_seg_ids_json(directory):
    seg_ids_file = join(directory, 'seg_ids.json')
    if not exists(seg_ids_file):
        return None
    with open(seg_ids_file, 'r') as file:
        return json.load(file)

def generate_json(directory):
    seg_ids = read_seg_ids_json(directory)
    all_files = os.listdir(directory)
    model_files = [f for f in all_files if not f.startswith('.') and 
                   (fnmatch.fnmatch(f, '*.ply') or fnmatch.fnmatch(f, '*.glb') or 
                    fnmatch.fnmatch(f, '*.stl') or fnmatch.fnmatch(f, '*.fbx') or 
                    fnmatch.fnmatch(f, '*.obj'))]  # 加入對 *.obj 檔案的處理
    
    common_prefix = find_common_prefix(model_files)

    distinct_colors = generate_distinct_colors(len(model_files))
    color_index = 0

    data = []
    if seg_ids:
        for item in seg_ids:
            filename = item['filename']
            if filename not in model_files:
                continue

            name_without_extension = splitext(filename)[0]
            cleaned_name = name_without_extension.replace(common_prefix, '', 1)
            
            color = distinct_colors[color_index]
            color_index += 1

            segment = {
                "label": cleaned_name,
                "filename": filename,
                "color": {
                    "r": color["r"],
                    "g": color["g"],
                    "b": color["b"],
                    "a": 0.7
                }
            }
            data.append(segment)
    else:
        for filename in model_files:
            name_without_extension = splitext(filename)[0]
            cleaned_name = name_without_extension.replace(common_prefix, '', 1)
            
            color = distinct_colors[color_index]
            color_index += 1

            segment = {
                "label": cleaned_name,
                "filename": filename,
                "color": {
                    "r": color["r"],
                    "g": color["g"],
                    "b": color["b"],
                    "a": 0.7
                }
            }
            data.append(segment)

    print(f"加入的模型檔案數量: {len(data)}")

    output_file = join(directory, 'model_meta.json')

    if exists(output_file):
        os.remove(output_file)
    
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="在指定目錄生成模型元數據 JSON 檔案。")
    parser.add_argument('--path', type=str, required=True, help='JSON 檔案將被創建的目錄路徑，並包含檔案。')

    args = parser.parse_args()

    generate_json(args.path)

if __name__ == "__main__":
    main()
