import json
import os

# 存储所有 JSON 文件的内容
merged_data = []

# 遍历所有 JSON 文件
for filename in os.listdir(r'C:\Users\Xue\OneDrive\0_Code\demo\HR'):
    if filename.endswith('.json'):
        with open(os.path.join(r'C:\Users\Xue\OneDrive\0_Code\demo\HR', filename), 'r', encoding='utf-8') as file:
            # 读取 JSON 文件内容并解析为 JSON 数组
            try:
                data_array = json.loads(file.read())
                # 遍历 JSON 数组中的每个 JSON 对象
                for data in data_array:
                    # 将每个 JSON 对象添加到 merged_data 中
                    if isinstance(data, dict):
                        merged_data.append(data)
                    else:
                        print(f"Skipping {filename}: Content is not a valid dictionary.")
            except json.JSONDecodeError:
                print(f"Skipping {filename}: Failed to decode JSON content.")

# 将合并后的内容写入新的 JSON 文件
with open('merged_data.json', 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)
