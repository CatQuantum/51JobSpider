import pandas as pd
import json
import os

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

    # 根据'requirement'列的前两项分别拆分为'exp'和'edu'，然后删除原来的'requirement'列
    #df[['exp', 'edu']] = pd.DataFrame(df['requirement'].tolist(), index=df.index)[[0, 1]]
    #df.drop(columns=['requirement'], inplace=True)

    # 将修改后的DataFrame保存为Excel文件
    excel_path = file_path.replace('.json', '.xlsx')
    df.to_excel(excel_path, index=False)

    print(f"文件已保存为 {excel_path}")


if __name__ == "__main__":


    # 指定需要遍历的文件夹路径
    folder_path = r'C:\Users\Xue\Documents\GitHub\gender-discrimination-hiring\Add_com\to_be_send'

    json2excel_all(folder_path)