# -*- coding: utf-8 -*-
import scrapy
from summon.items import SummonItem

class ExampleSpider(scrapy.Spider):
    name = 'getAllSecurities'
    allowed_domains = ['dfcfw.com']
    start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(Code)&sortRule=1&page=1&pageSize=10000&js=var%20ndayATVq={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1524201658073']

    def parse(self, response):
        body = response.body.decode()
        sep1, sep2 = '["', '"]'
        i1 = body.index(sep1) + 2
        i2 = body.index(sep2) 
        s = body[i1:i2].split('","')
        res = []

        for elem in s:
            items = elem.split(',')
            item = SummonItem()
            item['securityID'] = items[1]
            item['marketID'] = items[0]
            item['securityKey'] = item['securityID'] + '.' + item['marketID']
            item['name'] = items[2]
            res.append(item)
            yield item

        
# //*[@id="common_table"]/tbody/tr[1]/td[2]/a

# http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?sortType=(Code)&page=1&pageSize=200000&js=res={rank:[(x)],pages:(pc),total:(tot)}

# http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(Code)&sortRule=1&page=1&pageSize=2000&js=var%20ndayATVq={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1524201658073
# http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(Code)&sortRule=1&page=1&pageSize=10000&js=var%20ndayATVq={rank:[(x)],pages:(pc),total:(tot)}&jsName=quote_123&_g=0.628606915911589&_=1524201658073