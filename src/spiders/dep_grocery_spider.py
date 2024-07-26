import scrapy
from src.store.grocery_items import WalmartGroceryItem
from src.common.URLs import urls
import json


class WalmartSpider(scrapy.Spider):
    name = "walmart_grocery"
    BASE_URL = 'https://www.walmart.com'
    start_urls = urls
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'COOKIES_ENABLED': False,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': True,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        script_tag = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag:
            json_blob = json.loads(script_tag)
            count = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["count"]
            for item in range(count):
                item_data = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"][item]
                if "canonicalUrl" in item_data:
                    sub_links = item_data["canonicalUrl"]
                    print("sub_links", sub_links)
                    full_url = response.urljoin(sub_links)
                    yield scrapy.Request(full_url, callback=self.parse_product)
                else:
                    print(f"Item {item} does not have a canonicalUrl")

        current_page = int(response.url.split('page=')[1].split('&')[0])
        next_page_url = response.url.replace(
            f'page={current_page}', f'page={current_page + 1}')

        if current_page < 1:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        self.logger.info(f"Processing product page: {response.url}")
        # Parse json blob
        script_tag = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag:
            json_blob = json.loads(script_tag)

        try:
            # Extract product details props.pageProps.initialData.data.product
            product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
            # props.pageProps.initialData.data.idml
            product_idml = json_blob["props"]["pageProps"]["initialData"]["data"]["idml"]
            title = response.css('h1#main-title::text').get()
            title = title.strip() if title else 'N/A'
            price = response.css('span[itemprop="price"]::text').get()
            price = price.replace('Now ', '') if price else 'N/A'
            off_price = response.css(
                'span.mr2.f6.gray.mr1.strike::text').get() or 'N/A'
            rating_raw = response.css('span.rating-number::text').get()
            rating = rating_raw.strip('()') if rating_raw else 'N/A'
            badge = response.css(
                'span.w_VbBP.w_mFV6.w_I_19.w_3oNC.w_AAn7.tag-leading-badge::text').get() or 'N/A'
            keywords = response.css('span[itemprop="name"]::text').getall()
            reviews = response.css(
                'a[data-testid="item-review-section-link"]::text').get()
            reviews = reviews.replace(
                'reviews', '').strip() if reviews else 'N/A'
            returns_back = response.css(
                'li[data-testid="free-returns"] span.f7::text').get() or 'N/A'

            grocery_item = WalmartGroceryItem(
                id=product_data.get('id'),
                title=title,
                product_url=response.url,
                img_url_list=product_data.get('imageInfo').get('allImages'),
                price=price,
                brand=product_data.get('brand'),
                off_price=off_price,
                shortDescription=product_data.get('shortDescription'),
                longDescription=product_idml.get('longDescription'),
                productHighlights=product_idml.get('productHighlights'),
                specifications=product_idml.get('specifications'),
                warranty=product_idml.get('warranty'),
                rating=rating,
                badge=badge,
                returns_back=returns_back,
                reviews=reviews,
                availabilityStatus=product_data.get('availabilityStatus'),
                availableQuantity=product_data.get('fulfillmentOptions', [{}])[
                    0].get('availableQuantity', 'N/A'),
                manufacturerProductId=product_data.get(
                    'manufacturerProductId'),
                model=product_data.get('model'),
                type=product_data.get('type'),
                conditionType=product_data.get('conditionType'),
                sellerId=product_data.get('sellerId'),
                offerId=product_data.get('offerId'),
                offerType=product_data.get('offerType'),
                orderLimit=product_data.get('orderLimit'),
                sellerType=product_data.get('sellerType'),
                upc=product_data.get('upc'),
                sellerDisplayName=product_data.get('sellerDisplayName'),
                sellerName=product_data.get('sellerName'),
                location=product_data.get('location'),
                productTypeId=product_data.get('productTypeId'),
                numberOfReviews=product_data.get('numberOfReviews'),
                returnPolicy=product_data.get('returnPolicy'),
                salesUnit=product_data.get('salesUnit'),
                keywords=[keyword.strip()
                          for keyword in keywords] if keywords else 'N/A',
                category=product_data.get('category'),
                ingredients=product_idml.get('ingredients'),
                nutritionFacts=product_idml.get('nutritionFacts'),
                drugGuide=product_idml.get('drugGuide'),
            )
            yield grocery_item
        except Exception as e:
            self.logger.error(f"Error parsing product page: {e}")
