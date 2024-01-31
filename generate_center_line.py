import argparse
import pandas as pd
import json
import os

# 定義一個函數來將 CSV 數據轉換為指定的 JSON 格式
def convert_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, header=None)

    points = []
    paths = []
    point_index = {}

    for index, row in df.iterrows():
        # 使用 .iloc 來按位置訪問數據
        start_key = (row.iloc[0], row.iloc[1], row.iloc[2])
        end_key = (row.iloc[3], row.iloc[4], row.iloc[5])

        if start_key not in point_index:
            point_index[start_key] = len(points)
            points.append({"x": start_key[0], "y": start_key[1], "z": start_key[2]})

        if end_key not in point_index:
            point_index[end_key] = len(points)
            points.append({"x": end_key[0], "y": end_key[1], "z": end_key[2]})

        paths.append({"Start": point_index[start_key], "End": point_index[end_key]})

    return {
        "Vertices": points,
        "Edges": paths,
        "DefaultPath": {
            "Start": 0,
            "End": len(points) - 1
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to JSON.')
    parser.add_argument('--csv', required=True, help='Path to the CSV file')
    parser.add_argument('--json', required=True, help='Path to output JSON file')

    args = parser.parse_args()

    # 檢查 JSON 檔案是否已經存在，若存在則刪除
    if os.path.exists(args.json):
        os.remove(args.json)

    json_data = convert_to_json(args.csv)

    with open(args.json, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

if __name__ == "__main__":
    main()
