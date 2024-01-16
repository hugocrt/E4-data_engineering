# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):

    def process_item(self, item, spider):
        if item['ranking']:
            item['ranking'] = to_numeric(item['ranking'])
            return item
        else:
            raise DropItem(f'Not a valid ranking in {item}')


def to_numeric(string):
    res_str = ''.join(filter(str.isdigit, string))
    return int(res_str)


class MongoPipeline(object):
    collection_name = 'movies'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client['senscritique']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
