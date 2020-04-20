# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import JockeyItem
from HKJC_database.models import Jockey

class JockeysCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JockeyItem):
            #jockey_item = item.save(commit=False)
            Jockey_exist = Jockey.objects.filter(name= item['name'],
                                                 chinese_name= item['chinese_name'],
                                                 hkjc_id= item['hkjc_id']
                                                 )
            if not Jockey_exist: # save the jockey if it is not in the db
                item.save()
                pass
            else:
                pass

        return item
