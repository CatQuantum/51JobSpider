import json
import os

def merge_json_items(directory_path):
    all_items = []  # 用于存储所有文件中的items项

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        items = data['resultbody']['job']['items']
                        all_items.extend(items)
                except json.JSONDecodeError:
                    print(f"无法解析JSON文件：{file_path}")
                except KeyError:
                    print(f"找不到预期的键在文件：{file_path}")

    with open(os.path.join(directory_path, 'merged_items.json'), 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=4)

directory_path = 'Data_HR'
merge_json_items(directory_path)
