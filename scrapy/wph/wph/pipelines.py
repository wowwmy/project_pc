# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import redis
from hashlib import md5


class WphPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client.wph
        self.rouge = self.db.rouge
        self.redis = redis.Redis(host='localhost', port=6379, db=5)

    def process_item(self, item, spider):
        data = dict(item)
        md = md5(str(data).encode('utf-8')).hexdigest()
        if self.redis.sismember('wph', md):
            pass
        else:
            self.rouge.insert_one(data)
            self.redis.sadd('wph', md)
        return item

    def close_spider(self, spider):
        self.redis.close()
        self.client.close()
