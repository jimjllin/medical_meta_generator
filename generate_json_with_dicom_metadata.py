import argparse
import json
import pydicom

def read_dicom_metadata(dicom_file):
    try:
        ds = pydicom.dcmread(dicom_file, force=True)
        metadata = {
            "Patient ID": ds.PatientID,
            "Patient Name": str(ds.PatientName),
            "Patient Birth Date": ds.get("PatientBirthDate", "未知"),
            "Study Description": ds.get("StudyDescription", "未知")
        }
        return metadata
    except Exception as e:
        print(f"讀取 DICOM 檔案時發生錯誤: {e}")
        return {}



def combine_json(dicom_metadata, input_json, output_json):
    with open(input_json, 'r') as file:
        data = json.load(file)

    # 創建一個新的物件，包含 meta_data 和原來的列表
    combined_data = {
        "meta_data": dicom_metadata,
        "models": data
    }

    with open(output_json, 'w') as file:
        json.dump(combined_data, file, indent=4)



def main():
    parser = argparse.ArgumentParser(description='Combine DICOM metadata with JSON file.')
    parser.add_argument('--dicom', required=True, help='DICOM file path')
    parser.add_argument('--input_json', required=True, help='Input JSON file path')
    parser.add_argument('--output_json', required=True, help='Output JSON file path')

    args = parser.parse_args()

    dicom_metadata = read_dicom_metadata(args.dicom)
    combine_json(dicom_metadata, args.input_json, args.output_json)

if __name__ == "__main__":
    main()
