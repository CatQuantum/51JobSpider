import pandas as pd
import json
import os
from glob import glob
import random
import math

# 定义一个函数来读取 JSON 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def merge_json_files(input_folder, output_file):
    # """
    # 合并原始的页面文件
    # input_folder = r'C:\Users\Xue\OneDrive\0_Code\data\2024-4-6-1800-2000\original_data_copy'  # 替换为你的输入文件夹路径
    # output_file = r'C:\Users\Xue\OneDrive\0_Code\data\2024-4-6-1800-2000\merge.json'  # 替换为你想要保存合并后JSON的路径

    # merge_json_files(input_folder, output_file) 
    # """
    # 创建一个列表来保存所有文件中的数据
    all_data = []
    
    # 遍历文件夹下的所有JSON文件（包括子文件夹）
    for json_file_path in glob(os.path.join(input_folder, '**/*.json'), recursive=True):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            # 加载JSON数据并添加到all_data列表
            data = json.load(json_file)
            all_data.extend(data)
    
    # 写入合并后的数据到输出文件
    with open(output_file, 'w', encoding='utf-8') as output_json_file:
        json.dump(all_data, output_json_file, ensure_ascii=False, indent=4)


def process_merged_data(merged_data_path,processed_data_path):
    # """ 
    # 从合并的页面文件中提取需要的信息
    # merged_data_path=r'C:\Users\Xue\OneDrive\0_Code\data\2024-4-6-1800-2000\merge.json'
    # processed_data_path='processed_jobs.json'
    # """
    merged_data=read_json_file(merged_data_path)

    processed_data = []
    for item in merged_data:
        # 确保条目是字典类型
        if isinstance(item, dict):
            # 提取需要的字段
            processed_item = {
                "jobId": item.get("jobId"),
                "jobName": item.get("jobName"),
                "jobAreaString": item.get("jobAreaString"),
                "provideSalaryString": item.get("provideSalaryString"),
                "issueDateString": item.get("issueDateString"),
                "workYearString": item.get("workYearString"),
                "degreeString": item.get("degreeString"),
                "fullCompanyName": item.get("fullCompanyName"),
                "companyTypeString": item.get("companyTypeString"),
                "companySizeString": item.get("companySizeString"),
                "jobHref": item.get("jobHref"),
                "termStr": item.get("termStr"),
                "jobWelfareCodeDataList": [welfare.get("chineseTitle") for welfare in item.get("jobWelfareCodeDataList", []) if isinstance(welfare, dict)]
            }
            processed_data.append(processed_item)
        else:
            print(f"Warning: Non-dict item found in merged_data: {item}")

    with open(processed_data_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)



def random_split_json_array(file_path, num_files=6):
    
    # 读取原始JSON文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 随机打乱数组
    random.shuffle(data)

    # 计算每份数据的大小
    total_items = len(data)
    items_per_file = math.ceil(total_items / num_files)

    # 获取原始文件所在目录
    original_dir = os.path.dirname(file_path)

    # 分割并保存到新的JSON文件，文件保存在原始文件同目录
    for i in range(num_files):
        start_index = i * items_per_file
        end_index = min(start_index + items_per_file, total_items)
        split_data = data[start_index:end_index]

        # 构造新文件路径
        new_file_path = os.path.join(original_dir, f'random_part_{i+1}.json')

        with open(new_file_path, 'w', encoding='utf-8') as split_file:
            json.dump(split_data, split_file, indent=4, ensure_ascii=False)


def json2excel_all(folder_path):
        
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

def json2excel(file_path):
    # 从文件中加载JSON数据
    #file_path = r'C:\Users\Xue\OneDrive\0_Code\Spider\demo\Test\IT_and_split\IT.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 将JSON对象转换为pandas DataFrame
    df = pd.json_normalize(data)

    excel_path = file_path.replace('.json', '.xlsx')
    df.to_excel(excel_path, index=False)

    print(f"文件已保存为 {excel_path}")

def json2json(input_file_path,output_file_path):

    # 读取原始JSON数组文件
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 创建一个新的字典，使用索引作为键
    indexed_data = {str(i): item for i, item in enumerate(data)}

    # 将新的字典写入到一个新的JSON文件中
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(indexed_data, file, ensure_ascii=False, indent=4)

    print(f"文件已成功转换并保存为 {output_file_path}")




if __name__ == "__main__":

    # """ 
    # # 指定需要遍历的文件夹路径
    # folder_path = r'C:\Users\Xue\Documents\GitHub\gender-discrimination-hiring\Add_com\to_be_send'

    # json2excel_all(folder_path)
    print()
    