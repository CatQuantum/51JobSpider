import json
import random
import datetime
import os
import math

# 假定 JSON 文件的路径
file_path = r'C:\Users\Xue\OneDrive\0_Code\Spider\demo\Test\IT_and_split\merged_IT.json'

# 提取输入文件名（不包含扩展名）
base_name = os.path.basename(file_path)  # 获取文件名和扩展名：'Test.json'
file_name_without_extension = os.path.splitext(base_name)[0]  # 分离文件名和扩展名，取第一部分：'Test'

# 构造新的文件路径
new_file_name = f'Cleaned_{file_name_without_extension}.json'  # 新文件名：'Cleaned_Test.json'
# 假设你想将新文件保存在同一目录下
new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)


# 定义一个函数来读取 JSON 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


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


def parse_and_average_salary(salary):
    # 将薪资字符串中的“千”和“万”统一转换为浮点数（以“万”为单位）
    salary = salary.replace('千', '*0.1').replace('万', '')
    
    # 分割薪资范围
    salary_range = salary.split('-')
    
    # 计算薪资范围的平均值
    if len(salary_range) == 2:
        min_salary, max_salary = salary_range
        average_salary = ((eval(min_salary) + eval(max_salary)) *10000)/ 2
    else:
        average_salary = eval(salary_range[0])
    
    return round(average_salary, 2)  # 返回四舍五入后的平均薪资

def transform_salary_description(salary_desc):
    # 检查是否包含"及以下"
    if '及以下' in salary_desc:
        # 提取数值和单位
        value, unit = salary_desc.split('及以下')
        # 构造新的范围描述
        new_salary_desc = f"0-{value}{unit}"
        return new_salary_desc
    else:
        # 如果不包含"及以下"，则不需要转换
        return salary_desc

def calculate_monthly_salary(salary):
    salary=transform_salary_description(salary)
    if '年' in salary:
        # 年薪
        salary = salary.replace('/年', '')
        average_annual_salary = parse_and_average_salary(salary)
        return average_annual_salary / 12  # 转换为月薪
    elif '薪' in salary:
        # n薪
        salary_range, months = salary.split('·')
        average_salary = parse_and_average_salary(salary_range)
        months = float(months.replace('薪', ''))
        return average_salary * months / 12  # 计算年薪再转换为月薪
    elif '-' in salary:
        average_salary=parse_and_average_salary(salary)
        return average_salary
    else:
        # 不属于上述情况
        return None


# 使用函数读取 JSON 文件
data = read_json_file(file_path)

# 设定起始日期
start_date_str = '2024-03-13'
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

# 处理逻辑
company_jobs = {}
for job in data:
    # 将 issue_date 从字符串转换为 datetime 对象
    issue_date = datetime.strptime(job["issue_date"], "%Y-%m-%d %H:%M:%S")
    # 计算 issue_date 和 start_date 之间的差异
    date_diff = (issue_date - start_date).days

    monthly_salary = calculate_monthly_salary(job["salary"])
    if monthly_salary is not None:
        job["monthly_salary"] = monthly_salary

        if "实习" not in job["job_title"] and "本科" in job.get("requirement", [""])[1] and date_diff <= 30 and job["monthly_salary"]<40000:

            job["work_area"] = job["work_area"].split('·')[0]
            # 处理 requirement 字段，分别提取到 exp 和 edu，然后删除原 requirement
            if len(job["requirement"]) >= 2:
                job["exp"], job["edu"] = job["requirement"][:2]
            elif len(job["requirement"]) == 1:
                job["exp"] = job["requirement"][0]
                job["edu"] = ""  # 如果只有一项要求，默认第二项为空
            else:
                job["exp"] = job["edu"] = ""  # 如果没有要求，默认两项都为空
            del job["requirement"]  # 删除原来的 requirement 字段
            
                    # 在这里加入对 edu 字段的检查，仅保留包含“本科”的职位信息
            if "本科" in job["edu"]:
                if job["company_name"] in company_jobs:
                    company_jobs[job["company_name"]].append(job)
                else:
                    company_jobs[job["company_name"]] = [job]

# 随机选择一个职位项
randomized_data = [random.choice(jobs) for jobs in company_jobs.values()]

# 输出处理后的数据以确认
#print(json.dumps(randomized_data, ensure_ascii=False, indent=4))


# 将处理后的数据保存到新的 JSON 文件中
with open(new_file_path, 'w', encoding='utf-8') as new_file:
    json.dump(randomized_data, new_file, ensure_ascii=False, indent=4)



# 处理后的数据再随机分割为6份
random_split_json_array(new_file_path)
