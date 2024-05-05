import json


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
                "jobHref": item.get("jobHref"),
                "termStr": item.get("termStr"),
                "industryType1Str":item.get("industryType1Str"),
                "jobWelfareCodeDataList": [welfare.get("chineseTitle") for welfare in item.get("jobWelfareCodeDataList", []) if isinstance(welfare, dict)]
            }
            processed_data.append(processed_item)
        else:
            print(f"Warning: Non-dict item found in merged_data: {item}")

    return processed_data

merged_data_path=r'C:\Users\Xue\Documents\GitHub\gender-discrimination-hiring\Data_HR\merged_items.json'


# 假设merged_data是已经从文件中加载的数据
with open(merged_data_path, 'r', encoding='utf-8') as file:
    merged_data = json.load(file)

processed_data = process_merged_data(merged_data)



# 将处理后的数据保存到新文件
with open('processed_jobs.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)



'/mnt/data/processed_jobs.json'
