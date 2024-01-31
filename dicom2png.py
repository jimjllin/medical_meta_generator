import os
import argparse
import pydicom
from PIL import Image
import numpy as np

def convert_dicom_to_png(dicom_path, output_path):
    """將DICOM檔案轉換為PNG檔案。"""
    ds = pydicom.dcmread(dicom_path)
    pixel_array = ds.pixel_array
    image = Image.fromarray(np.uint8(pixel_array))
    print(image.size)
    image.save(output_path)

def main(directory):
    """處理指定資料夾中的所有DICOM檔案。"""
    for filename in os.listdir(directory):
        if filename.endswith(".dcm"):
            dicom_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, filename.replace('.dcm', '.png'))
            convert_dicom_to_png(dicom_path, output_path)
            print(f"{dicom_path} -> {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="將DICOM檔案轉換為PNG檔案。")
    parser.add_argument("--dir", type=str, required=True, help="包含DICOM檔案的資料夾路徑。")
    args = parser.parse_args()
    main(args.dir)
