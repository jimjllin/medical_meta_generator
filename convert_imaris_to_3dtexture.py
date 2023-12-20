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
        # 確定通道數量
        base_path = 'DataSet/ResolutionLevel 0/TimePoint 0/'
        channels = [key for key in file[base_path].keys() if key.startswith('Channel ')]
        num_channels = len(channels)
        print(f"總共發現 {num_channels} 個通道。")

        # 選擇要讀取的通道
        channel_to_read = 0  # 例如，這裡選擇第一個通道
        data_path = f'{base_path}Channel {channel_to_read}/Data'
        data = file[data_path][()]

    print(f"Voxel 尺寸: {data.shape}")
    print(f"數據類型: {data.dtype}")
    print("讀取完成。")
    return data



def convert_to_raw(data, output_filename):
    """
    將 3D 數據轉換為 raw 格式並保存到文件。
    """
    print("開始轉換數據為 raw 格式...")
    
    data = data.astype(np.uint8)
    data_bytes = data.tobytes()
    with open(output_filename, 'wb') as file:
        file.write(data_bytes)
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
