from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
from time import sleep
import re
from lxml import etree
import requests
import os
import json
import pandas as pd
import numpy as np

url_login = "https://login.51job.com/login.php?loginway=0&isjump=0&lang=c&from_domain=i&url="
# url_sh = "https://search.51job.com/list/020000,000000,0000,00,9,99,+,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
url_sh = "https://search.51job.com/list/020000%252c010000%252c030200%252c040000,000000,0000,00,9,99,+,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

email = 'credentials for 51job'
password = 'credentials for 51job'

df = pd.read_excel('zhength24M_L.xlsx')
key_words = df['company+postion'].values

lst_applied = []


def login():
    driver.get(url_login)
    driver.find_element_by_id("loginname").send_keys(email)
    driver.find_element_by_id("password").send_keys(password)
    for i in range(1):  # why i need to click twice?
        driver.find_element_by_id("login_btn").click()


def apply():
    for key_word in key_words:
        try:
            driver.get(url_sh)
            sleep(2)
            driver.find_element_by_id("keywordInput").send_keys(key_word)
            driver.find_element_by_id("search_btn").click()
            sleep(3)
            ActionChains(driver).move_to_element(
                driver.find_element_by_class_name("er")).perform()

            position_str = driver.find_element_by_xpath(
                "/html/body/div[2]/div[3]/div/div[1]/div[2]/div[2]").get_attribute('textContent')
            print (position_str)
            num_str = re.findall('[0-9]+', position_str)[0]
            if num_str == '1':
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]/div/div[2]/button").click()
                sleep(3)
                applied = 1
            else:
                applied = 0
        except:
            print ('Error')
            applied = 0
        lst_applied.append(applied)
        print (key_word)
        print (applied)


login()
apply()
print (sum(lst_applied) / len(lst_applied))
df['applied'] = lst_applied
df.to_csv('zhength_applied.csv', encoding='utf-8-sig')
