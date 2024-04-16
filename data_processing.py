import json
import json
import random
from datetime import datetime
import os
import math
import file_processing
from file_processing import *


def clean_data_jobName(data):
    # 清洗数据：去除包含“实习”或“intern”的职位
    cleaned_data = [item for item in data if "实习" not in item["jobName"] and "intern" not in item["jobName"].lower()]

    return cleaned_data
    

def transform_salary_description(salary_desc):
    # 检查是否包含"及以下"，以及是千还是万
    if '千及以下' in salary_desc:
        value, _ = salary_desc.split('千及以下')
        min_value = round(float(value) * 0.6, 5)  # 计算下限并四舍五入到5位小数
        new_salary_desc = f"{min_value}-{value}千"
    elif '万及以下' in salary_desc:
        value, _ = salary_desc.split('万及以下')
        min_value = round(float(value) * 0.6, 5)  # 计算下限并四舍五入到5位小数
        new_salary_desc = f"{min_value}-{value}万"
    else:
        # 如果不符合上述任一条件，则不需要转换
        return salary_desc
    
    return new_salary_desc


def parse_and_average_salary(salary):
    # 将薪资字符串中的“千”和“万”统一转换为浮点数（以“万”为单位）
    if "万" in salary:
        salary = salary.replace('千', '*0.1').replace('万', '')
        # 分割薪资范围
        salary_range = salary.split('-')
        # 计算薪资范围的平均值
        if len(salary_range) == 2:
            min_salary, max_salary = salary_range
            average_salary = ((eval(min_salary) + eval(max_salary)) * 10000) / 2
        else:
            average_salary = eval(salary_range[0]) * 10000
        return round(average_salary , 2)  # 返回平均薪资，单位为元
    #仅含"千"
    else:
        salary = salary.replace('千', '')
        salary_range = salary.split('-')
        if len(salary_range) == 2:
            min_salary, max_salary = salary_range
            average_salary = ((eval(min_salary) + eval(max_salary)) * 1000) / 2
        else:
            average_salary = eval(salary_range[0]) * 1000
        return round(average_salary , 2)  # 返回平均薪资，单位为元


def calculate_monthly_salary(salary_string):
    # 假设transform_salary_description已经将薪资描述转换为了易于解析的格式
    salary_string=transform_salary_description(salary_string)
    if '年' in salary_string:
        salary_string = salary_string.replace('/年', '')
        average_annual_salary = parse_and_average_salary(salary_string)
        return round(average_annual_salary / 12, 2)  # 转换为月薪
    elif '薪' in salary_string:
        salary_range, months = salary_string.split('·')
        average_salary = parse_and_average_salary(salary_range)
        months = float(months.replace('薪', ''))
        return round(average_salary * months / 12, 2)  # 计算年薪再转换为月薪
    elif '-' in salary_string:
        return parse_and_average_salary(salary_string)  # 直接返回月薪
    else:
        # 不属于上述情况，可能需要进一步处理
        print(salary_string)
        return None



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



data=read_json_file(r'C:\Users\Xue\OneDrive\0_Code\Spider\demo\AC\jobs_data_2024-03-10_14-52-17area_030200_type_0457.json')