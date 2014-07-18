import scrapy
from scrapy.spider import BaseSpider
from sets import Set
from scrapy import log
from weixin.items  import WeixinArticle
import cgi

class GZHTop3(BaseSpider):
    name = "gzhtop3"
    allowed_domains = []
    start_urls = [
        "http://weixin.sogou.com/gzhwap?openid=oIWsFty5GrTq6kuv7Ny-PhQSOQh0"
        ]
    
    def parse(self, response):
        print response.url
        title = response.xpath("//title/text()").extract()[0]
        print title
        href = response.xpath("//a/@href").extract()
##        print href
        hrefInSet = Set()
        
        for h in href:
##            str = h.encode('ascii', 'ignore')
            #print type(str)
            if h.startswith("http://mp.weixin.qq.com"):
                #print h
                hrefInSet.add(h)

        print hrefInSet
        print len(hrefInSet)
        for urlItem in hrefInSet:
            yield scrapy.Request(url = urlItem, callback = self.parseItem)

    def parseItem(self, response):
        article = WeixinArticle()
        url = response.url
        title = response.xpath('//*[@id="activity-name"]/text()').extract()[0]
        time = response.xpath('//*[@id="post-date"]/text()').extract()[0]
        gzh = response.xpath('//*[@id="post-user"]/span/text()').extract()[0]
        content = response.xpath('//*[@id="page-content"]').extract()[0]

        article['url'] = cgi.escape(url)
        article['title'] = cgi.escape(title)
        article['time'] = cgi.escape(time)
        article['gzh'] =cgi.escape(gzh)
        article['content'] = cgi.escape(content)
        return article
##        yield article
