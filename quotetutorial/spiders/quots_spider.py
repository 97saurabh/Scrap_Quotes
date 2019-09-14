import scrapy
from scrapy.http import FormRequest

from ..items import QuotetutorialItem
class QuoteSpider(scrapy.Spider):
    name="quotes"
    start_urls=[
        "http://quotes.toscrape.com/login"
    ]
    def parse(self,response):
        token=response.css("form input::attr(value)").extract_first()
        return FormRequest.from_response(response,formdata={"csrf_token":token,"username":"Saurabh@gmail.com","password":"GYSDJHSGJHDS"},callback=self.start_scrapy)


    def start_scrapy(self,response):
        iteams=QuotetutorialItem()
        all_div_tags = response.css("div.quote")
        for quote in all_div_tags:
            title=quote.css("span.text::text").extract()
            author=quote.css(".author::text").extract()
            tags=quote.css(".tag::text").extract()
            #print("DATA",title,author,tags)
            iteams["title"]=title
            iteams["author"]=author
            iteams["tags"]=tags
            yield iteams
        next_page=response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.start_scrapy)
