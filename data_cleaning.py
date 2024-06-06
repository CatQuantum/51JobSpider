import json
import os
import random
from datetime import datetime
import os
import math


# 定义一个函数来读取 JSON 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data



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
        print("异常值为:",salary_string)
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
    return all_items

def process_merged_data(merged_data):
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
                "companyIndustryType1Str": item.get("companyIndustryType1Str"),
                "companyIndustryType2Str": item.get("companyIndustryType2Str"),
                "jobHref": item.get("jobHref"),
                "termStr": item.get("termStr"),
                "industryType1Str":item.get("industryType1Str"),
                "jobWelfareCodeDataList": [welfare.get("chineseTitle") for welfare in item.get("jobWelfareCodeDataList", []) if isinstance(welfare, dict)]
            }
            processed_data.append(processed_item)
        else:
            print(f"Warning: Non-dict item found in merged_data: {item}")

    return processed_data




#抓取的原始文件目录路径
directory_path = r'D:\WorkFile\51job_data\2024\Data_Ac\Original_AC'

merged_data=merge_json_items(directory_path)
processed_data=process_merged_data(merged_data)


# 设定起始日期
start_date_str = '2024-5-19'
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')


#工作地点在北上广深
#30天以内
#月薪小于40000
#去掉应届生

company_jobs = {}
for job in processed_data:

    job["jobAreaString"] = job["jobAreaString"].split('·')[0]
    
    if job["jobAreaString"] in ["北京","上海","广州","深圳"]:

        if "应届" not in job["jobName"] :


            # 将 issue_date 从字符串转换为 datetime 对象

            issue_date = datetime.strptime(job["issueDateString"], "%Y-%m-%d %H:%M:%S")

            # 计算 issue_date 和 start_date 之间的差异
            date_diff = (start_date - issue_date).days

            monthly_salary = calculate_monthly_salary(job["provideSalaryString"])
            if monthly_salary is not None:
                job["monthly_salary"] = monthly_salary
            else:
                job["monthly_salary"] = -1


            if date_diff < 30 and (job["monthly_salary"]<40000 ):

                if job["workYearString"] != "在校生/应届生":

                    if job["fullCompanyName"] in company_jobs:
                        company_jobs[job["fullCompanyName"]].append(job)
                    else:
                        company_jobs[job["fullCompanyName"]] = [job]

# 随机选择一个职位项
randomized_data = [random.choice(jobs) for jobs in company_jobs.values()]


with open(os.path.join(directory_path, 'merged_data.json'), 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

# 将处理后的数据保存到新文件
with open(os.path.join(directory_path, 'processed_data.json'), 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)


# 将处理后的数据保存到新的 JSON 文件中
with open(os.path.join(directory_path, 'cleaned_data.json'), 'w', encoding='utf-8') as new_file:
    json.dump(randomized_data, new_file, ensure_ascii=False, indent=4)

# 处理后的数据再随机分割为6份
random_split_json_array(os.path.join(directory_path, 'cleaned_data.json'))