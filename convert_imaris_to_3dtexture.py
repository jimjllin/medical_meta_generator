import numpy as np
import h5py
import argparse

def read_ims_file(filename):
    """
    從 .ims 檔案中讀取數據。

    參數:
    filename (str): .ims 檔案的路徑。

    返回:
    numpy.ndarray: 從檔案中讀取的數據。
    """
    print("開始讀取 .ims 檔案...")
    with h5py.File(filename, 'r') as file:
        # 根據你的檔案結構調整這個路徑
        data_path = 'DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'
        dataset = file[data_path]
        data_shape = dataset.shape
        data = np.empty(data_shape, dtype=dataset.dtype)

        for i in range(data_shape[2]):
            data[:, :, i] = dataset[:, :, i]
            print(f"已讀取層 {i + 1}/{data_shape[2]}")

    print(f"Voxel 尺寸: {data.shape}")
    print("讀取完成。")
    return data


def convert_to_raw(data, output_filename):
    """
    將 3D 數據轉換為 raw 格式並保存到文件。
    """
    print("開始轉換數據為 raw 格式...")
    data = data.astype(np.uint8)
    depth = data.shape[2]  # 取得數據的深度

    with open(output_filename, 'wb') as file:
        for i in range(depth):
            # 處理每一層並寫入文件
            file.write(data[:, :, i].tobytes())
            print(f"已轉換並寫入層 {i + 1}/{depth}")

    print(f"文件 '{output_filename}' 已生成.")

def main():
    parser = argparse.ArgumentParser(description='將 Imaris .ims 檔案轉換為 Unity 的 3D texture raw 格式。')
    parser.add_argument('--input', type=str, required=True, help='輸入的 .ims 檔案路徑')
    parser.add_argument('--output', type=str, required=True, help='輸出的 raw 檔案路徑')

    args = parser.parse_args()

    data = read_ims_file(args.input)
    convert_to_raw(data, args.output)

if __name__ == "__main__":
    main()
