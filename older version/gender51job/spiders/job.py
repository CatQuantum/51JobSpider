# -*- coding: utf-8 -*-
import json
import re
import scrapy
from gender51job.items import Gender51JobItem


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['search.51job.com']

    def start_requests(self):
        urls = []
        # note that the url changes sometime, everytime use this go and find the lastest url. Not only change the range.
        # # # AC
        # for i in range(1, 1508):
        #     url = f"https://search.51job.com/list/020000%252c010000%252c030200%252c040000,000000,0400,00,9,99,+,2,{i}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        # # # IT
        # for i in range(1, 2001):
        #     url = f"https://search.51job.com/list/020000%252c010000%252c030200%252c040000,000000,7700%252c7200%252c2700%252c6600%252c8000,00,9,99,+,2,{i}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        # # HR
        for i in range(1, 1657):
            url = f"https://search.51job.com/list/040000%252c020000%252c010000%252c030200,000000,0600,00,9,99,+,2,{i}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="

            urls.append(url)
        for j in urls:
            yield scrapy.Request(url=j, callback=self.parse)

    def parse(self, response):
        body = response.body.decode("gbk")
        data = re.findall(
            'window.__SEARCH_RESULT__ =(.+)</script>', str(body))[0]
        data = json.loads(data)
        item = Gender51JobItem()
        for var in data["engine_search_result"]:
            item["job_title"] = var["job_title"]
            item["company_name"] = var["company_name"]
            item["salary"] = var["providesalary_text"]
            item["work_area"] = var["workarea_text"]
            item["company_type"] = var["companytype_text"]
            item["is_intern"] = var["isIntern"]
            item["issue_date"] = var["issuedate"]
            item["job_welf"] = var["jobwelf_list"]
            item["requirement"] = var["attribute_text"][1:]
            item["company_size"] = var["companysize_text"]
            item["company_industry"] = var["companyind_text"]
            yield item  
        pass
