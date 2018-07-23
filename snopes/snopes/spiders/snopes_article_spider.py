import scrapy
import re
from snopes.items import SnopesItem


class snopesArticleSpider(scrapy.Spider):
    name = "snopesarticle"

    first_page = True

    start_urls = [
        "https://www.snopes.com/news/",
        "https://www.snopes.com/news/page/",
    ]

    def parse_article(self, response):
        item = SnopesItem()
        item['title'] = response.css("h1.article-title::text").extract_first()
        item['author'] = response.css("span.author::text").extract_first() or response.css("a.author::text").extract_first()
        item['date'] = response.css("span.post-date::text").extract_first()
        item['text'] = '\n'.join(response.css("div.article-text-inner p::text").extract())
        item['wordcount'] = len(re.findall(r'\w+', item['text']))
        return item

    def parse(self, response):
        for href in response.css("div.list-wrapper article a").xpath("@href").extract():
            yield scrapy.Request(href, callback=self.parse_article)

        if self.first_page is True:
            next_page = response.css("div.article-list-pagination a").xpath("@href").extract_first()
            self.first_page = False
        else:
            next_page = response.css("div.article-list-pagination a").xpath("@href").extract()[1]
        print("this is the next page")
        print(next_page)
        """print("The isolated URL is:")
        print(next_page[28:])"""
        if next_page is not '':
            """print("combining URLs..................................")
            url = response.urljoin(next_page[28:])
            print("the URL is:")
            print(url)"""
            yield scrapy.Request(next_page, self.parse)

