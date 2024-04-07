# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Gender51JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    work_area = scrapy.Field()
    company_type = scrapy.Field()
    is_intern = scrapy.Field()
    issue_date = scrapy.Field()
    job_welf = scrapy.Field()
    requirement = scrapy.Field()
    company_size = scrapy.Field()
    company_industry = scrapy.Field()
    pass
