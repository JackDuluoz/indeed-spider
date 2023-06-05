import scrapy
from scrapy_playwright.page import PageMethod
from pathlib import Path

class QuotesSpider(scrapy.Spider):
    name = 'indeed'

    def start_requests(self):
        url = 'https://ca.indeed.com/'
        yield scrapy.Request(url, meta=dict(
            playwright = True,
            playwright_include_page = True,
            # playwright_page_methods =[PageMethod('wait_for_selector', 'div.jobsearch-TabbedContent-container')],
            errback=self.errback, 
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        filename = f"indeed.html"
        Path(filename).write_bytes(response.body)
        yield {
                'span': response.css("span::text").getall()
            }
        
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    # def start_requests(self):
    #     url = "https://ca.indeed.com/"
    #     yield scrapy.Request(url, meta=dict(
    #             playwright = True,
    #             playwright_include_page = True, 
    #             playwright_page_methods =[
    #                 PageMethod('wait_for_selector', 'head'),
    #             ],
    #     errback=self.errback,
    #         ))
    # async def parse(self, response):
    #     page = response.meta["playwright_page"]
    #     await page.close()
    #     yield {
    #             'title': response.css("head title::text").get()
    #         }
  
    # async def errback(self, failure):
    #     page = failure.request.meta["playwright_page"]
    #     await page.close()