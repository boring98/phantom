import json
import scrapy
from summon.items import CandlestickItem
from summon.items import SummonItem

class ExampleSpider(scrapy.Spider):
    name = 'kday'

    allowed_domains = ['dfcfw.com']
    start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(Code)&sortRule=1&page=1&pageSize=10000&js=var%20ndayATVq={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1524201658073']

    def parse(self, response):
        body = response.body.decode()
        sep1, sep2 = '["', '"]'
        i1 = body.index(sep1) + 2
        i2 = body.index(sep2) 
        s = body[i1:i2].split('","')

        for elem in s:
            items = elem.split(',')
            securityKey = items[1] + items[0]
            url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id={0}&type=k&authorityType=fa'.format(securityKey)
            yield scrapy.Request(url=url, callback=self.parseCandlestick, dont_filter=True)

    def parseCandlestick(self, response):
        body = response.body.decode()[1: -1]
        res = json.loads(body)

        item = CandlestickItem()
        item['securityKey'] = res['code'] + '.' + res['info']['jys']
        item['data'] = res['data']
        yield item
        

