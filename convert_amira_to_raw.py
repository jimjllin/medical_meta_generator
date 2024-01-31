from PIL import Image
import argparse

def process_tiff(input_path, output_path):
    try:
        # 打開 TIFF 檔案
        with Image.open(input_path) as img:
            # 輸出圖像的一些基本資訊
            print(f"圖像格式: {img.format}")
            print(f"圖像大小: {img.size}")
            print(f"圖像模式: {img.mode}")

            # 處理圖像...
            # 例如，轉換為灰階
            img = img.convert('L')

            # 儲存圖像
            img.save(output_path)
            print(f"圖像已儲存為 {output_path}")

    except IOError:
        print(f"無法打開檔案: {input_path}")
    except Exception as e:
        print(f"處理檔案時發生錯誤: {e}")

# 解析命令列參數
parser = argparse.ArgumentParser(description="處理 TIFF 格式的檔案")
parser.add_argument("--input", required=True, help="TIFF 檔案的輸入路徑")
parser.add_argument("--output", required=True, help="處理後的檔案輸出路徑")
args = parser.parse_args()

process_tiff(args.input, args.output)
