# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from summon import settings


class SummonPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            charset='utf8mb4',
        )
        # self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('replace into security(securityKey, securityID, marketID, name) values (%s, %s, %s, %s)', (
                    item['securityKey'], item['securityID'], item['marketID'], item['name']))
            self.connection.commit()
        except Exception as error:
            print('Found Error: ', error)
            # print(error)
        return item
