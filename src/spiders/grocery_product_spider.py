from typing import Any
import scrapy
from scrapy.http import Response
import json


class WalmartSpider(scrapy.Spider):
    name = "walmart_products"
    BASE_URL = 'https://www.walmart.com'
    url = ['https://www.walmart.com/browse/electronics/3944']

    def start_requests(self):
        for url in self.url:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag:
            json_blob = json.loads(script_tag)
            count = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["count"]
            for item in range(count):
                item_data = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"][item]
                if "canonicalUrl" in item_data:
                    sub_links = item_data["canonicalUrl"]
                    print("sub_links", sub_links)
                else:
                    print(f"Item {item} does not have a canonicalUrl")
