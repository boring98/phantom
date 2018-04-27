import scrapy
from summon.items import KDayItem

class ExampleSpider(scrapy.Spider):
    name = 'kday'
    allowed_domains = ['dfcfw.com']
    start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(Code)&sortRule=1&page=1&pageSize=10000&js=var%20ndayATVq={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1524201658073']

# http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id=6013181&type=k&authorityType=fa

    def parse(self, response):
        body = response.body.decode()
        sep1, sep2 = '["', '"]'
        i1 = body.index(sep1) + 2
        i2 = body.index(sep2) 
        s = body[i1:i2].split('","')
        res = []

        for elem in s:
            items = elem.split(',')
            item = KDayItem()
            item['securityID'] = items[1]
            item['marketID'] = items[0]
            item['securityKey'] = item['securityID'] + '.' + item['marketID']
            item['name'] = items[2]
            res.append(item)
            yield item

        