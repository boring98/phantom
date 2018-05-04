# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from summon import settings
from summon.items import CandlestickItem
from summon.items import SummonItem


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
        if item.__class__ == SummonItem:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute('replace into security(securityKey, securityID, marketID, name) values (%s, %s, %s, %s)', (
                        item['securityKey'], item['securityID'], item['marketID'], item['name']))
                self.connection.commit()
            except Exception as error:
                print('Found Error: ', error)
                # print(error)
            return item
        elif item.__class__ == CandlestickItem:
            try:
                preClose = 0
                sqlStatList = []
                for data in item['data']:
                    raw = data.split(',')
                    #  0:date    , 1:open, 2:close, 3:high, 4:low, 5:volume, 6:turnover, 7:振幅, 8:换手%
                    # "2018-04-26, 65.68 , 63.12  , 65.89 , 62.81, 841554  , 53.6亿    , 4.7%  , 0.78",
                    oneSQLStat = '''
                        ('{securityKey}', '{date}', {kid}, {preClose}, {open}, {close}, {high}, {low}, {volume}, {turnover}, '{marketTime}')
                    '''.format(securityKey=item['securityKey'], date=raw[0], kid=-1, preClose=preClose, open=raw[1], close=raw[2], high=raw[3], low=raw[4], volume=getOriginalDigital(raw[5]), turnover=getOriginalDigital(raw[6]), marketTime=raw[0])
                    sqlStatList.append(oneSQLStat)
                    preClose = raw[2]
                    # item['date'] = raw[0]
                    # item['kid'] = -1
                    # item['preClose'] = preClose
                    # item['open'] = raw[1]
                    # item['close'] = raw[2]
                    # item['high'] = raw[3]
                    # item['low'] = raw[4]
                    # item['volume'] = getOriginalDigital(raw[5])
                    # item['turnover'] = getOriginalDigital(raw[6])
                    # item['marketTime'] = raw[0]
                if len(sqlStatList) != 0:
                    sqlstat = 'replace into candlestick(securityKey, date, kid, preClose, open, close, high, low, volume, turnover, marketTime) values ' + ','.join(sqlStatList)
                    with self.connection.cursor() as cursor:
                        cursor.execute(sqlstat)
                    self.connection.commit()
            except Exception as error:
                print('Found Error: ', error)
                # print(error)
            return item
        else:
            print('No such class!!!!')


def getOriginalDigital(digitalWithChinese):
    c = digitalWithChinese[-1]
    d = digitalWithChinese[: -1]
    if c == '万':
        res = float(d) * 10000
    elif c == '亿':
        res = float(d) * 10000 * 10000
    else:
        res = float(digitalWithChinese)
    return res
