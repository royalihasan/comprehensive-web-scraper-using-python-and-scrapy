import scrapy
from src.store.grocery_items import WalmartGroceryItem
from src.common.URLs import urls

class WalmartSpider(scrapy.Spider):
    name = "walmart_grocery"
    BASE_URL = 'https://www.walmart.com'
    urls = urls

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
            )

    def parse(self, response):
        category = response.url.split('/')[4]  # Extract category from URL
        links = response.css('a.hide-sibling-opacity::attr(href)').getall()
        for link in links:
            full_url = response.urljoin(link)
            # print('URL:', full_url) #DEBUG
            if "track" not in full_url:  # Check if "track" is not in the URL
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_product
                )

        # Dynamically generate the next page URL
        current_page = int(response.url.split('page=')[1].split('&')[0])
        next_page_url = response.url.replace(
            f'page={current_page}', f'page={current_page + 1}')

        if current_page < 9:  # Set the number of pages to scrape
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )

    def parse_product(self, response):
        # print('Parsing product page:', response.url) #DEBUG
        try:
            heading = response.css('h1#main-title::text').get()
            title = heading.strip() if heading else 'N/A'
            brand = response.css('div.mt0.mh0-l.mh3 a::text').get()
            image_url = response.css(
                'div[data-testid="media-thumbnail"] img::attr(src)').get()
            image_url_2x = response.css(
                'div[data-testid="media-thumbnail"] img::attr(srcset)').re_first(r'(https://[^\s]+) 2x')

            price = response.css(
                'span[itemprop="price"]::text').get().replace('Now ', '')
            off_price = response.css('span.mr2.f6.gray.mr1.strike::text').get()

            product_details = response.xpath(
                '//*[@id="product-description-section"]/section/div[2]/div/div/div[1]/span/div/text()').get()

            rating_raw = response.css('span.rating-number::text').get()

            # Remove the brackets from the rating text
            rating = rating_raw.strip('()') if rating_raw else None

            badge = response.css(
                'span.w_VbBP.w_mFV6.w_I_19.w_3oNC.w_AAn7.tag-leading-badge::text').get()

            keywords = response.css('span[itemprop="name"]::text').getall()
            reviews = response.css(
                'a[data-testid="item-review-section-link"]::text').get().replace('reviews', '').strip()
            keyword_list = [keyword.strip() for keyword in keywords]
            returns_back = response.css(
                'li[data-testid="free-returns"] span.f7::text').get()
            # make image urls dictionary
            image_urls = {}
            if image_url:
                image_urls['1x'] = image_url
            if image_url_2x:
                image_urls['2x'] = image_url_2x

            grocery_item = WalmartGroceryItem(
                title=title, product_url=response.url,
                brand=brand if brand else 'N/A',
                img_url=image_urls if image_url else 'N/A',
                price=price if price else 'N/A',
                off_price=off_price if off_price else 'N/A',
                product_details=product_details if product_details else 'N/A',
                rating=rating if rating else 'N/A',
                badge=badge if badge else 'N/A',
                returns_back=returns_back if returns_back else 'N/A',
                reviews=reviews if reviews else 'N/A',
                keywords=keyword_list if keyword_list else 'N/A'


            )
            yield grocery_item
        except Exception as e:
            self.logger.error(f"Error parsing product page: {e}")
