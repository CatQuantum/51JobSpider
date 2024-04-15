from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import json
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from time import sleep
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import random




#检查页面是否含有职位元素
def check_jobs_existence(driver, combination, completed_combinations_set):
    """
    检查页面是否含有职位元素，基于特定的文本提示或类名。
    
    :param driver: WebDriver实例，用于页面操作。
    :param combination: 当前检查的组合标识。
    :param completed_combinations_set: 已完成组合的集合。
    :return: 布尔值，True表示页面上存在职位列表，False表示没有找到职位。
    """
    wait = WebDriverWait(driver, timeout=60, poll_frequency=0.5)
    # 等待直到加载指示器不可见
    loading_indicator_locator = (By.CSS_SELECTOR, ".van-toast--loading")
    wait.until(EC.invisibility_of_element_located(loading_indicator_locator))

    try:
        # 尝试基于类名找到表示没有职位的特定元素
        driver.find_element(By.CLASS_NAME, "j_nolist")
        # 或者，使用提供的XPath路径
        # driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div")
        
        # 如果找到了该元素，说明没有职位
        print("没有找到职位，跳过此次循环。")
        with open('completed_combinations.txt', 'a') as file:
            file.write(combination + '\n')
        completed_combinations_set.add(combination)
        print(f"组合 {combination} 已记录至completed_combinations.txt文件。")
        return False
    except TimeoutException:
        # 如果等待页面加载的元素超时
        print("等待页面加载完毕超时，可能页面未完全加载。")
        return False
    except NoSuchElementException:
        # 如果没有找到特定元素，说明页面上有职位列表
        print("职位列表存在，继续处理。")
        return True
    
   

#检查页面是否加载完毕
def check_page_loaded(driver, timeout=60, poll_frequency=0.5):
    """
    检查页面是否加载完毕，基于预定义的条件：等待最后一页的分页元素可点击，
    并且加载指示器不可见。

    :param driver: WebDriver实例。
    :param timeout: 超时时间，默认60秒。
    :param poll_frequency: 轮询频率，默认0.5秒。
    :return: 布尔值，True表示页面加载完毕，False表示加载超时。
    """
    wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)

    try:
        # 等待最后一页的分页元素变为可点击
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.el-pager li.number:last-child")))

        # 等待直到加载指示器不可见
        loading_indicator_locator = (By.CSS_SELECTOR, ".van-toast--loading")
        wait.until(EC.invisibility_of_element_located(loading_indicator_locator))

        # 等待职位列表项变为可点击
        joblist_item_locator = (By.CSS_SELECTOR, ".joblist-item-job")
        wait.until(EC.element_to_be_clickable(joblist_item_locator))

        return True  # 页面加载完毕
    
    except TimeoutException:
        return False  # 页面加载超时



#轮询等待
def wait_for_file(folder_path, page, timeout=30, poll_interval=0.5):
    """
    等待直到特定页面的文件在指定文件夹中出现，或超时。

    :param folder_path: 文件夹路径。
    :param page: 页面编号。
    :param timeout: 最长等待时间（秒）。
    :param poll_interval: 轮询间隔时间（秒）。
    :return: 布尔值，True表示文件已找到，False表示超时。
    """
    start_time = time.time()
    while time.time() - start_time <= timeout:
        if file_exists_in_folder(folder_path, page):
            return True
        time.sleep(poll_interval)
    return False


def file_exists_in_folder(folder_path, page):
    """
    检查特定页码的文件是否存在于文件夹中。
    """
    for filename in os.listdir(folder_path):
        if f"_{page}_" in filename:
            return True
    return False


#翻页功能
def page_turning(driver,combination):

    """
    遍历页面的分页。
    
    :param driver: WebDriver实例，用于页面操作。
    :param combination: 用于标识不同文件夹/文件组合的标识符。

    """

    folder_path = os.path.join(os.getcwd(), str(combination))  # 构建文件夹路径

    try:
        last_page_element = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number:last-child")
        total_pages = int(last_page_element.text)
    except NoSuchElementException:
        print("无法找到分页元素，检查选择器或页面结构。")
        return 

    for page in range(1, total_pages + 1):
        if page > 1:
            try:
                jump_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "jump_page"))
                )
                jump_page.clear()
                jump_page.send_keys(page)
                
                jump_button = driver.find_element(By.CSS_SELECTOR, ".jumpPage")
                jump_button.click()
                sleep_time=random.uniform(0.5,2.0)
                sleep(sleep_time)

                if check_page_loaded(driver, timeout=60, poll_frequency=0.5):
                    if not wait_for_file(folder_path, page):
                        print(f"等待页面 {page} 对应的文件超时，文件未在文件夹 {folder_path} 中找到。")
                        driver.refresh()  # 刷新一下，重新抓取
                

            except (NoSuchElementException, TimeoutException) as e:
                print(f"在尝试跳转到页面 {page} 时发生错误: {e}")
                break  # 如果出现错误，终止循环   
    return 


def check_pages_catch(url,combination,completed_combinations_set):
    if combination in completed_combinations_set:
        return True # 跳过已完成的组合
    
    if (combination+"-溢出") in completed_combinations_set:
        return False

    driver.get(url)

    if check_jobs_existence(driver, combination, completed_combinations_set):
        if check_page_loaded(driver, timeout=60, poll_frequency=0.5):
            driver.refresh()
    else:
        return True #若无岗位列表，则退出该次循环

    #检查是否加载完毕
    if check_page_loaded(driver, timeout=60, poll_frequency=0.5):

        last_page_element = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number:last-child")
        total_pages = int(last_page_element.text)
        if total_pages!=50:
            page_turning(driver,combination)
            
            #记录保存组合
            with open('completed_combinations.txt', 'a') as file:
                file.write(combination + '\n')
            completed_combinations_set.add(combination)
            print(f"组合已记录至completed_combinations.txt文件。")

            return True
        else:
            combination=combination+"-溢出"
            with open('completed_combinations.txt', 'a') as file:
                file.write(combination + '\n')
            completed_combinations_set.add(combination)
            print(f"溢出组合已记录至completed_combinations.txt文件。")
            return False
            #溢出了，跳出该循环，进入下一级筛选



def click_to_check():

    """
    通过点击来切换页面，暂未完成，不稳定，未使用
    """

    element_to_click_xpaths =[
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[2]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[3]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[4]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[5]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[6]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[6]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[7]/span',
    '/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[3]/div[4]/div/div[2]/a[8]/span',
    ]

    if total_pages==50:
        open_selection_path='/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/div[4]/span'
        open_selection = wait.until(EC.element_to_be_clickable((By.XPATH, open_selection_path)))
        #open_selection.click()  


        # 等待直到加载指示器不可见
        wait.until(EC.invisibility_of_element_located(loading_indicator_locator))


        open_selection = driver.find_element(By.XPATH, open_selection_path)
        open_selection.click()
        
        size=0
        for element_to_click_xpath in element_to_click_xpaths:
            #sleep(5)
            element_to_click = driver.find_element(By.XPATH, element_to_click_xpath)


            # 等待直到加载指示器不可见
            wait.until(EC.invisibility_of_element_located(loading_indicator_locator))

            #element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, element_to_click_xpath)))
            element_to_click.click()                    
        #这里可以读取
        # 假设您已经有了一个名为driver的WebDriver实例
            
            ''''
            WebDriverWait(driver, 10).until(
                lambda x: driver.execute_script("return document.readyState") == "complete"
            )
            '''
            

            #last_page_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.el-pager li.number:last-child")))


            # 等待直到加载指示器不可见
            wait.until(EC.invisibility_of_element_located(loading_indicator_locator))
            sleep(3)
            last_page_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.el-pager li.number:last-child")))

            last_page_element = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number:last-child")
            total_pages = int(last_page_element.text)
            size=size+1
            print(function,area,size,total_pages)
    else:
        print(function,area,total_pages)    




if __name__ == "__main__":


    # 设置日志记录的配置
    logging.basicConfig(filename='script.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)



    options = ChromeOptions()
    #使用代理服务器，便于用Mitmproxy监听
    options.add_argument("--proxy-server=http://localhost:8080")
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


    jobArea=['040000', '020000', '010000', '030200']

    function_Ac=['0404', '0405', '2D01', '2D02', '2D03', '0448', '0457']

    function_HR=['0601', '0602', '0611', '0603', '0604', '0605', '0626', '0606', '0609', '0610', '0629', '0607', '0608', '0627', '0628', '0630', '0635']


    function_IT = {
        "Backend_Development_0100": ['0107', '0106', '0121', '0156', '0157', '0153', '0126', '0152', '0124', '0120', '0151', '0158', '0154', '0143', '0130', '0117', '0133', '0155', '0123', '0131', '0132', '0128'],
        "Operation_Technical_Support_7900": ['7909', '7908', '7901', '7915', '7920', '7913', '7912', '7905', '7902', '7906', '0149', '7914', '7904', '7903', '0150', '7910', '7907', '7918', '7916', '7917'],
        "Technical_Management_2600": ['2610', '2608', '2607', '2606', '2605', '7912', '7908', '7502', '2705', '2726', '2604', '2603', '2611', '2612'],
        "Test_2700": ['2725', '2723', '2705', '2726', '2707', '2957', '2718', '2704', '2722', '2720', '2719', '2706', '2724', '7821', '2816'],
        "Artificial_Intelligence_7300": ['7309', '7307', '7301', '7302', '7120', '7308', '7306'],
        "Front_end_development_7200": ['7201', '7202'],
        "Data_7500": ['7501', '7502', '7503', '7506', '7508', '7504', '7512', '7507', '7505', '7511', '7510'],
        "Mobile_development_7700": ['7701', '7702', '7703', '7705'],
        "Game_7800": ['7811', '7823', '7810', '7809'],
        "Sales_technical_support_8400": ['8401', '8402', '8403', '8404']
    }

    companySize=['01','02','03','04','05','06','07']

    jobAreas = ['010000', '020000', '040000', '030200']  
    # jobArea代码
    # 040000 深圳
    # 020000 上海
    # 010000 北京
    # 030200 广州



    base_url = "https://we.51job.com/pc/search?searchType=2&sortType=0&metro=&degree=04,07&jobType=01"
    #基础url中已筛选，degree=04,07（本科，无学历要求），jobType=01（01，全职工作。注意，“全职工作”包括全职实习，需要后续进行数据清洗）



    completed_combinations_set = set()
    combination=''

    ########################



    #同一文件夹下的completed_combinations.txt记录了已爬取的组合
    try:
        with open(r'completed_combinations.txt', 'r') as file:
            for line in file:
                completed_combinations_set.add(line.strip())
        print("completed combinations file found")
    except FileNotFoundError:
        print("No completed combinations file found, starting fresh.")



    for list_name, function_codes in function_IT.items():
        for function in function_codes:
            combination=f"{function}-010000,020000,040000,030200-"
            
            url = f"{base_url}&jobArea=010000,020000,040000,030200&function={function}" 


            if not check_pages_catch(url,combination,completed_combinations_set):

                for area in jobArea:
                    combination= f"{function}-{area}-"
                    url = f"{base_url}&jobArea={area}&function={function}" 
                    
                    if not check_pages_catch(url,combination,completed_combinations_set):
                        for Size in companySize:
                            combination=f"{function}-{area}-{Size}"
                            url=f"{base_url}&jobArea={area}&function={function}&companySize={Size}" 
                            
                            if not check_pages_catch(url,combination,completed_combinations_set):
                                print("三级筛选依然溢出")


                
                

