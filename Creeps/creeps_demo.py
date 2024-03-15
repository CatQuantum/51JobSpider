from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from time import sleep
import json
import logging
import datetime



# 设置日志记录的配置
logging.basicConfig(filename='script.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)





chromedriver_path = r"C:\chromedriver-win64\chromedriver.exe"

# 假设 `jobs_data` 是包含所有职位信息的列表
jobs_data = []


""" try:
    times = int(input("输入需要爬取的数量，没有输入则爬取所有岗位"))
except ValueError:
    times = float('inf')  # 设置为无限大，表示爬取所有职位
 """

times = float('inf')

#times = int(input("需要爬取的数量:"));


# 创建Service对象，并传入ChromeDriver的路径
service = Service(executable_path=chromedriver_path)

# 使用Service对象初始化Chrome WebDriver
driver = webdriver.Chrome(service=service)


from selenium.webdriver.chrome.options import Options

# 选择 Chrome 浏览器并打开
options = Options()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

# 假设点击之前只有一个窗口
original_window = driver.current_window_handle
assert len(driver.window_handles) == 1

# 获取当前时间
now = datetime.datetime.now()
# 格式化时间字符串，例如：2024-03-09_12-30-00
formatted_time = now.strftime('%Y-%m-%d_%H-%M-%S')


from selenium.common.exceptions import NoSuchElementException

def fetch_job_details(driver, date, job_type):
    # 等待页面加载
    wait = WebDriverWait(driver, 10)
    
    job_url = driver.current_url

    try:
        job_title = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/h1").get_attribute('title')

    except NoSuchElementException:
        input_flag = int(input("遇到意料外的页面需要处理(1:已处理/2:退出当前页面处理下一条):"))
        if input_flag == 0:
            print("未排除错误, 已关闭并存储, 读取下一条")
            write_error_urls(job_url)
            return {}
        else:
            try:
                job_title = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/h1").get_attribute('title')
            except NoSuchElementException:
                print("未排除错误, 已关闭并存储, 读取下一条")
                write_error_urls(job_url)
                return {}

    
    company_name = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[2]/div[1]/a/p").get_attribute('title')
    
    salary = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/strong").text
    
    details = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/p').get_attribute('title')
    # 由于原始字符串使用了"&nbsp;"作为空格和"|&nbsp;"作为分隔符，可能需要替换或直接分割
    print(details)
    details_parts = details.replace('\xa0\xa0', ' ').split(' | ')
    print(details_parts)
    work_area = None
    experience = None
    education = None

    if len(details_parts) > 0:
        work_area = details_parts[0]
    if len(details_parts) > 1:
        experience = details_parts[1]
    if len(details_parts) > 2:
        education = details_parts[2]

    company_type = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[2]/div[2]/p[1]").get_attribute('title')
    
    is_intern = ""
    
    issue_date = date
    
    # 使用find_elements来找到所有匹配的<span>元素
    benefits_elements = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/div/span")

    # 遍历元素集合，提取每个元素的文本
    job_welf = [element.text for element in benefits_elements]
    
    requirement = [experience, education,""]
    
    company_size = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[2]/div[2]/p[2]").get_attribute('title')
    
    company_industry = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[2]/div[2]/p[3]").get_attribute('title')

    # 收集到的数据存入字典
    job_data = {
        "job_title": job_title,
        "company_name": company_name,
        "salary": salary,
        "work_area": work_area,
        "company_type": company_type,
        "is_intern": is_intern,
        "issue_date": issue_date,
        "job_welf": job_welf,
        "requirement": requirement,
        "company_size": company_size,
        "company_industry": company_industry,
        "job_url": job_url,
        "job_type":job_type
        # 添加更多字段...
    }
    print(job_data)
    
    return job_data

def wait_for_element_clickable(driver, by_method, selector, timeout=10):

    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by_method, selector))
    )

def crawl_current_page(driver, jobs_data, times):
    # 定位到职位元素列表
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".joblist-item")

    for job_element in job_elements:

        # 从元素获取sensorsdata属性，它是一个JSON格式的字符串
        job_elements_detail = job_element.find_element(By.CSS_SELECTOR, ".joblist-item-job")
        sensorsdata = job_elements_detail.get_attribute("sensorsdata")
        
        # 将JSON字符串解析为Python字典
        data = json.loads(sensorsdata.replace('&quot;', '"'))
        
        # 提取jobTime属性
        issue_time = data.get("jobTime")
        job_type = data.get("funcType")
        job_title = data.get("jobTitle")
        salary = data.get("jobSalary")
        work_area = data.get("jobArea")
        experience = data.get("jobYear")
        education = data.get("jobDegree")
        is_intern = ""
        
        try:
            job_tag = job_element.find_element(By.CSS_SELECTOR, ".tags")
            job_tags = job_tag.find_elements(By.CSS_SELECTOR, ".tag")
            job_welf = [element.text for element in job_tags]
        except:
            job_welf = []

        # 遍历元素集合，提取每个元素的文本
        
        requirement = [experience, education,""]

        company_elements_detail = job_element.find_element(By.CSS_SELECTOR, ".joblist-item-bot")

        company_name = company_elements_detail.find_element(By.CSS_SELECTOR, ".cname").text
        try:
            company_industry = company_elements_detail.find_element(By.CSS_SELECTOR, 'span.dc.text-cut').text
            try:
                company_type = company_elements_detail.find_elements(By.CSS_SELECTOR, 'span.dc.shrink-0')[0].text
            except:
                company_type = ''
            # 找到公司规模元素
            try:
                company_size = company_elements_detail.find_elements(By.CSS_SELECTOR, 'span.dc.shrink-0')[1].text
            except:
                company_size = ''
        except:
            try:
                company_type = company_elements_detail.find_elements(By.CSS_SELECTOR, 'span.dc.shrink-0')[1].text
            except:
                company_type = ''
            # 找到公司规模元素
            try:
                company_size = company_elements_detail.find_elements(By.CSS_SELECTOR, 'span.dc.shrink-0')[2].text
            except:
                company_size = ''
            try:
                company_industry = company_elements_detail.find_element(By.CSS_SELECTOR, 'span.dc.shrink-0')[0].text
            except:
                company_industry = ''
        # 找到公司类型元素
        

        # 获取当前所有打开的窗口句柄
        original_window_handles = driver.window_handles
        original_window = driver.current_window_handle

        # 模拟点击每个职位元素
        try:
            job_element.find_element(By.CSS_SELECTOR, ".joblist-item-top").click()
            print("click")
        except:
            print("click-error")
        sleep(1)
        wait = WebDriverWait(driver, 10)
        
        # 检查是否有新窗口打开
        new_window_handles = driver.window_handles
        new_windows = set(new_window_handles) - set(original_window_handles)

        if new_windows:
            print()        
        else:
             # 没有新窗口打开，等待10秒
            print("No new window opened. Waiting for 10 seconds.")
            sleep(10)

        current_url = ""
        try:             #change
            driver.switch_to.window(driver.window_handles[1])
            current_url = driver.current_url
        except:
            current_url = ""

        data = {
            "job_title": job_title,
            "company_name": company_name,
            "salary": salary,
            "work_area": work_area,
            "company_type": company_type,
            "is_intern": is_intern,
            "issue_date": issue_time,
            "job_welf": job_welf,
            "requirement": requirement,
            "company_size": company_size,
            "company_industry": company_industry,
            "job_url": current_url,
            "job_type":job_type
            # 添加更多字段...
        }

        jobs_data.append(data)

        print("成功抓取一个岗位信息")  # 输出调试信息
        print(data)
        if current_url != "":
            driver.close()  # 关闭当前的职位详细信息窗口
        driver.switch_to.window(driver.window_handles[0])  # 切换回职位列表的窗口

                    

        times = times - 1
        print("剩余:"+str(times))
        if times == 0:
            return times

    return times




jobArea=['040000', '020000', '010000', '030200']

function_Ac=['0404', '0405', '2D01', '2D02', '2D03', '0448', '0457']

function_HR=['0601', '0602', '0611', '0603', '0604', '0605', '0626', '0606', '0609', '0610', '0629', '0607', '0608', '0627', '0628', '0630', '0635']


function_IT = {
#    "Backend_Development_0100": ['0107', '0106', '0121', '0156', '0157', '0153', '0126', '0152', '0124', '0120', '0151', '0158', '0154', '0143', '0130', '0117', '0133', '0155', '0123', '0131', '0132', '0128'],
#    "Operation_Technical_Support_7900": ['7909', '7908', '7901', '7915', '7920', '7913', '7912', '7905', '7902', '7906', '0149', '7914', '7904', '7903', '0150', '7910', '7907', '7918', '7916', '7917'],
#    "Technical_Management_2600": ['2610', '2608', '2607', '2606', '2605', '7912', '7908', '7502', '2705', '2726', '2604', '2603', '2611', '2612'],
#    "Test_2700": ['2725', '2723', '2705', '2726', '2707', '2957', '2718', '2704', '2722', '2720', '2719', '2706', '2724', '7821', '2816'],
    # "Artificial_Intelligence_7300": ['7309', '7307', '7301', '7302', '7120', '7308', '7306'],
    "Front_end_development_7200": ['7201', '7202'],
    "Data_7500": ['7501', '7502', '7503', '7506', '7508', '7504', '7512', '7507', '7505', '7511', '7510'],
    "Mobile_development_7700": ['7701', '7702', '7703', '7705'],
    "Game_7800": ['7811', '7823', '7810', '7809'],
    "Sales_technical_support_8400": ['8401', '8402', '8403', '8404']
}

jobAreas = ['010000', '020000', '040000', '080000']  
# jobArea代码
# 040000 深圳
# 020000 上海
# 010000 北京
# 030200 广州

# 基础URL
base_url = "https://we.51job.com/pc/search?searchType=2&sortType=0&metro="

completed_combinations_set = set()

try:
    with open(r'C:\Users\Xue\OneDrive\0_Code\demo\completed_combinations.txt', 'r') as file:
        for line in file:
            completed_combinations_set.add(line.strip())
    print("completed combinations file found")
except FileNotFoundError:
    print("No completed combinations file found, starting fresh.")


for list_name, function_codes in function_IT.items():
    for function in function_codes:
        for area in jobArea:
            if (function in ('0107', '0106', '0121', '0156', '0157', '0153', '0126', '0152', '0124', '0120')):
                continue

            combination = f"{area}-{function}"
            
            if combination in completed_combinations_set:
                continue  # 跳过已完成的组合

            # 构建完整的URL
            url = f"{base_url}&jobArea={area}&function={function}" 
            #print("Visiting URL:", url)
            # 发送GET请求
            #urls.append(url)

            # 初始化Chrome WebDriver
            driver = webdriver.Chrome(options=options)

            # 打开目标网页
            driver.get(url)
            sleep(1)
            driver.refresh()
            sleep(5)

            

            try:
                # 尝试找到表示没有职位的特定文本元素
                no_jobs_element = driver.find_element(By.XPATH, "//*[contains(text(), '哦哦！没有职位不要怕，你那么年轻那么好看，再重搜一次呗~')]")
                print("没有找到职位，跳过此次循环。")
                with open('completed_combinations.txt', 'a') as file:
                    file.write(combination + '\n')
                completed_combinations_set.add(combination)
                print(f"组合已记录至completed_combinations.txt文件。")
                continue  # 如果找到了该元素，说明没有职位，跳过本次循环
            except NoSuchElementException:
                # 如果没有找到特定文本，说明页面上有职位列表，继续执行后面的代码
                print("职位列表存在，继续处理。")            
            
            # 确保首页职位列表被加载
            wait_for_element_clickable(driver, By.CSS_SELECTOR, ".joblist-item-job")




            #这里可以读取
            # 假设您已经有了一个名为driver的WebDriver实例
            last_page_element = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number:last-child")
            total_pages = int(last_page_element.text)



            for page in range(1, total_pages + 1):   
                if page > 1:  # 如果不是第一页，找到分页输入框，输入页码，然后点击跳转
                    jump_page = wait_for_element_clickable(driver, By.ID, "jump_page")
                    jump_page.clear()
                    jump_page.send_keys(page)
                    
                    jump_button = driver.find_element(By.CSS_SELECTOR, ".jumpPage")
                    jump_button.click()
                    
                    # 等待页面加载完毕
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".joblist-item-job"))
                    )
                
                times = crawl_current_page(driver, jobs_data, times)
                if times == 0:
                    break 

                print(f"完成第 {page} 页的抓取")
                

            # 完成所有任务后关闭浏览器
            driver.quit()

            # 获取当前时间
            now = datetime.datetime.now()
            # 格式化时间字符串，例如：2024-03-09_12-30-00
            formatted_time = now.strftime('%Y-%m-%d_%H-%M-%S')

            # 创建文件名，包含时间信息
            filename = f'jobs_data_type_{list_name}_{formatted_time}.json'

            # 使用新的文件名写入数据
            with open(filename, 'w', encoding='utf-8') as f:
                # 确保使用`ensure_ascii=False`以支持中文字符，pretty print 用于美化输出
                json.dump(jobs_data, f, ensure_ascii=False, indent=4)

            print(f"数据已导出到 '{filename}' 文件。")
            with open('completed_combinations.txt', 'a') as file:
                file.write(combination + '\n')
            completed_combinations_set.add(combination)
            print(f"组合已记录至completed_combinations.txt文件。")

#            except:



    jobs_data.clear()

