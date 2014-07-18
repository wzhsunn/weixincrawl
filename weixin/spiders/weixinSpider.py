import scrapy
from scrapy.spider import BaseSpider
from sets import Set
from scrapy import log
from weixin.items  import WeixinArticle
import cgi
from selenium import webdriver
from time import sleep

class WeiXinSpider(BaseSpider):
    name = "weixinspider"
    allowed_domains = []
    start_urls = [
##        "http://weixin.sogou.com/weixin?type=2&query=%E4%B8%96%E7%95%8C%E6%9D%AF"
##        "http://weixin.sogou.com/gzhwap?openid=oIWsFty5GrTq6kuv7Ny-PhQSOQh0"
        "http://weixin.sogou.com/gzh?openid=oIWsFty5GrTq6kuv7Ny-PhQSOQh0"
        ]
    
    def parse(self, response):
        print response.url
        browser = webdriver.Firefox()
        browser.get(response.url)
        sleep(5)
        browser.find_element_by_xpath('//*[@id="wxmore"]/a').click()
        sleep(5)
        html_source = browser.page_source
##        log.msg(html_source)
##        print html_source
        response = response.replace(body = html_source)
        title = response.xpath("//title/text()").extract()[0]
        print title
        href = response.xpath("//a/@href").extract()
##        href = browser.find_elements_by_xpath("//*[@href]")
        print href
        
        hrefInSet = Set()
        
        for h in href:
            if h.startswith("http://mp.weixin.qq.com"):
                #print h
                hrefInSet.add(h)

        print hrefInSet
        print len(hrefInSet)
        for urlItem in hrefInSet:
            yield scrapy.Request(url = urlItem, callback = self.parseItem)
        browser.close()
        
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
##        article['content'] = cgi.escape(content)
        return article
##        yield article
