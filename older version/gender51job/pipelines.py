# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter


class Gender51JobPipeline:
    def __init__(self):
        self.fp = open('result.json', 'w', encoding='utf-8') 

    def open_spider(self, spider):
        self.fp.write("[")

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False)
        self.fp.write(data+',\n')
        return item

    def close_spider(self, spider):
        self.fp.write("]")
        self.fp.close()
        print("spider end")