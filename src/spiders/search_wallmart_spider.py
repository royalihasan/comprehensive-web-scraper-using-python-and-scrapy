import json
import math
import scrapy
from urllib.parse import urlencode
from typing import Generator
from src.items import WalmartItem


class WalmartSpider(scrapy.Spider):
    name = "search_walmart"

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        keyword_list = ['laptop', 'smartphone', 'tablet', 'smartwatch',
                        'headphones', 'earbuds', 'speaker', 'monitor', 'keyboard', 'mouse']
        for keyword in keyword_list:
            payload = {
                'q': keyword,
                'sort': 'best_seller',
                'page': 1,
                'affinityOverride': 'default'
            }
            walmart_search_url = f'https://www.walmart.com/search?{
                urlencode(payload)}'
            yield scrapy.Request(
                url=walmart_search_url,
                callback=self.parse_search_results,
                meta={'keyword': keyword, 'page': 1}
            )

    def parse_search_results(self, response: scrapy.http.Response) -> Generator[scrapy.Request, None, None]:
        page = response.meta['page']
        keyword = response.meta['keyword']
        script_tag = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag:
            json_blob = json.loads(script_tag)

            try:
                product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
                for idx, product in enumerate(product_list):
                    walmart_product_url = f'https://www.walmart.com{
                        product.get("canonicalUrl", "").split("?")[0]}'
                    yield scrapy.Request(
                        url=walmart_product_url,
                        callback=self.parse_product_data,
                        meta={'keyword': keyword,
                              'page': page, 'position': idx + 1}
                    )

                if page == 1:
                    total_product_count = json_blob["props"]["pageProps"][
                        "initialData"]["searchResult"]["itemStacks"][0]["count"]
                    max_pages = min(2, math.ceil(total_product_count / 100000))
                    for p in range(2, max_pages + 1):
                        payload = {
                            'q': keyword,
                            'sort': 'best_seller',
                            'page': p,
                            'affinityOverride': 'default'
                        }
                        walmart_search_url = f'https://www.walmart.com/search?{
                            urlencode(payload)}'
                        yield scrapy.Request(
                            url=walmart_search_url,
                            callback=self.parse_search_results,
                            meta={'keyword': keyword, 'page': p}
                        )
            except (KeyError, IndexError) as e:
                self.logger.error(f"Error parsing search results: {e}")

    def parse_product_data(self, response: scrapy.http.Response) -> Generator[WalmartItem, None, None]:
        script_tag = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag:
            json_blob = json.loads(script_tag)
            try:
                raw_product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
                item = WalmartItem(
                    keyword=response.meta['keyword'],
                    page=response.meta['page'],
                    position=response.meta['position'],
                    id=raw_product_data.get('id'),
                    type=raw_product_data.get('type'),
                    name=raw_product_data.get('name'),
                    brand=raw_product_data.get('brand'),
                    averageRating=raw_product_data.get('averageRating'),
                    manufacturerName=raw_product_data.get('manufacturerName'),
                    shortDescription=raw_product_data.get('shortDescription'),
                    thumbnailUrl=raw_product_data['imageInfo'].get(
                        'thumbnailUrl'),
                    price=raw_product_data['priceInfo']['currentPrice'].get(
                        'price'),
                    currencyUnit=raw_product_data['priceInfo']['currentPrice'].get(
                        'currencyUnit'),
                )
                yield item
            except (KeyError, IndexError) as e:
                self.logger.error(f"Error parsing product data: {e}")
