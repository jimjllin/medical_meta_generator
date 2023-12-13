import json
import random
import argparse
import colorsys

def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7 + 0.3 * (i % 2)  # 交替選擇 70% 和 100% 的飽和度
        lightness = 0.5
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append({"r": r, "g": g, "b": b, "a": 0.7})
    random.shuffle(colors)
    return colors

def replace_colors(obj, colors):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                if 'r' in value and 'g' in value and 'b' in value:
                    color = random.choice(colors)
                    obj[key] = {"r": color["r"], "g": color["g"], "b": color["b"], "a": color["a"]}
                else:
                    replace_colors(value, colors)
            elif isinstance(value, list):
                for item in value:
                    replace_colors(item, colors)
    elif isinstance(obj, list):
        for item in obj:
            replace_colors(item, colors)

def main():
    parser = argparse.ArgumentParser(description='替換 JSON 檔案中的顏色。')
    parser.add_argument('--file', type=str, help='JSON 檔案的路徑', required=True)
    args = parser.parse_args()

    file_path = args.file
    with open(file_path, 'r') as file:
        data = json.load(file)

    colors = generate_distinct_colors(64)
    replace_colors(data, colors)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f'更新後的檔案已儲存到 {file_path}')

if __name__ == "__main__":
    main()
