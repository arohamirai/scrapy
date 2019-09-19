import scrapy


class QuotesSpider(scrapy.Spider):
    # identifies the Spider, it must be unique within a project
    name = "quotes"
    
    # must return an iterable of Requests 
    # 如果可以直接写出url，则可以直接定义给 start_urls 属性赋值
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            # create a Request to schedules and register the callback function
            yield scrapy.Request(url=url, callback=self.parse)

    # a method that will be called to handle the response downloaded for each of the requests made.
    # The response parameter is an instance of TextResponse that holds the page content and has further helpful methods to handle it.
    # The parse() method usually parses the response, extracting the scraped data as dicts and also finding new URLs to follow and creating new requests (Request) from them.
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        # 跟踪下一层链接
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
