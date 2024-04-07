import pandas as pd
import json
import os

# 指定需要遍历的文件夹路径
folder_path = r'C:\Users\Xue\OneDrive\0_Code\data'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否为JSON文件
    if filename.endswith('.json'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        
        # 加载JSON数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 将JSON对象转换为pandas DataFrame
        df = pd.json_normalize(data)
        

        # 构建Excel文件路径
        excel_path = file_path.replace('.json', '.xlsx')
        
        # 将DataFrame保存为Excel文件
        df.to_excel(excel_path, index=False)
        
        print(f"文件已保存为 {excel_path}")

