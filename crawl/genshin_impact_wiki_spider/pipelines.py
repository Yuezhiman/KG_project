import os
import shutil
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GenshinImpactWikiSpiderPipeline:
    def __init__(self):
        self.data_root = 'data'
        if os.path.exists(self.data_root):
            shutil.rmtree(self.data_root)
        os.makedirs(self.data_root)

    def process_item(self, item, spider):
        file_path = os.path.join(self.data_root, item['type'] + '.json')
        data = item['data']
        f = open(file_path, 'a', encoding = 'utf-8')
        f.write(json.dumps(data, ensure_ascii = False) + '\n')
        f.close()
        return item
