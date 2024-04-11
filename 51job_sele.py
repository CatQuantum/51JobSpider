from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
import json

import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import json
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import random
import json
import random
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# 定义保存数据的函数
def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



def get_competition(text):
    # 假设你已经用之前的方法获得了这个字符串,字符串样例示例：
    #text = "（排名129/364）"
    # 使用正则表达式匹配文本中的数字
    matches = re.findall(r'\d+', text)

    # 假设文本格式固定，排名和总人数都是数字，并且总人数在第二个位置
    if matches:
        total_number = matches[1]  # 获取总人数
        
    return total_number




options = ChromeOptions()
""" #使用代理服务器，便于用Mitmproxy监听
options.add_argument("--proxy-server=http://localhost:8080") """
# 忽略SSL错误
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
#禁用Blink引擎的某些特性，未指定
options.add_argument("--disable-blink-features")
#隐藏Selenium自动化控制的痕迹
options.add_argument("--disable-blink-features=AutomationControlled")

############
#无界面模式
#options.add_argument("--headless")
############

chromedriver_path = r"C:\chromedriver-win64\chromedriver.exe"


""" try:
    times = int(input("输入需要爬取的数量，没有输入则爬取所有岗位"))
except ValueError:
    times = float('inf')  # 设置为无限大，表示爬取所有职位
 """
times = float('inf')

# 创建Service对象，并传入ChromeDriver的路径
service = Service(executable_path=chromedriver_path)
# 使用Service对象初始化Chrome WebDriver
driver = webdriver.Chrome(service=service,options=options)

wait = WebDriverWait(driver, 60)

import os
import json

# 指定文件夹路径
folder_path = ''
# 初始化一个空字典来存储加载的JSON数据
data = {}

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否为JSON文件
    if filename.endswith('.json'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 加载JSON数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data[filename[:-5]] = json.load(file)

# 现在，`data`字典包含了所有JSON文件的数据，键是文件名（不包括扩展名）


for i in range(1, 7):
    for job in data[f'random_part_{i}']:
        if "在校生/应届生" in job['workYearString']:
            job['competition'] = "在校生/应届生数据，忽略抓取"
            save_data(data, f"修正/data_part_{i}.json")  # 立即保存数据
        else:
            if "competition" not in job:
                competition_url = f"https://i.51job.com/userset/compete.php?jobid={job['jobId']}&resumeid=468287804&accountid=241451461&lang=c"
                driver.get(competition_url)
                sleep_time = random.uniform(1.5, 2.5)
                sleep(sleep_time)
                try:
                    element_text = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/strong[2]').text
                    competition = get_competition(element_text)
                    job['competition'] = competition
                    save_data(data, f"修正/data_part_{i}.json")  # 立即保存数据
                except NoSuchElementException:
                    job['competition']='无competition数据'
                    print(job)
                except Exception as e:
                    sleep_time = random.uniform(1.5, 2.5)
                    sleep(sleep_time)
                    element_text = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/strong[2]').text
                    competition = get_competition(element_text)
                    job['competition'] = competition
                    save_data(data, f"修正/data_part_{i}.json")  # 立即保存数据
            