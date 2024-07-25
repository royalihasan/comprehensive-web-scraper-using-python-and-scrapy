import scrapy
from src.store.grocery_items import WalmartGroceryItem
from src.common.URLs import urls


class WalmartSpider(scrapy.Spider):
    name = "walmart_grocery"
    BASE_URL = 'https://www.walmart.com'
    start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        links = response.css('a.hide-sibling-opacity::attr(href)').getall()
        for link in links:
            full_url = response.urljoin(link)
            if "track" not in full_url:
                yield scrapy.Request(full_url, callback=self.parse_product)

        current_page = int(response.url.split('page=')[1].split('&')[0])
        next_page_url = response.url.replace(
            f'page={current_page}', f'page={current_page + 1}')

        if current_page < 9:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        try:
            title = response.css('h1#main-title::text').get().strip() or 'N/A'
            brand = response.css('div.mt0.mh0-l.mh3 a::text').get() or 'N/A'
            image_url = response.css(
                'div[data-testid="media-thumbnail"] img::attr(src)').get()
            image_url_2x = response.css(
                'div[data-testid="media-thumbnail"] img::attr(srcset)').re_first(r'(https://[^\s]+) 2x')
            price = response.css('span[itemprop="price"]::text').get().replace(
                'Now ', '') or 'N/A'
            off_price = response.css(
                'span.mr2.f6.gray.mr1.strike::text').get() or 'N/A'
            product_details = response.xpath(
                '//*[@id="product-description-section"]/section/div[2]/div/div/div[1]/span/div/text()').get() or 'N/A'
            rating_raw = response.css('span.rating-number::text').get()
            rating = rating_raw.strip('()') if rating_raw else 'N/A'
            badge = response.css(
                'span.w_VbBP.w_mFV6.w_I_19.w_3oNC.w_AAn7.tag-leading-badge::text').get() or 'N/A'
            keywords = response.css('span[itemprop="name"]::text').getall()
            reviews = response.css(
                'a[data-testid="item-review-section-link"]::text').get().replace('reviews', '').strip() or 'N/A'
            returns_back = response.css(
                'li[data-testid="free-returns"] span.f7::text').get() or 'N/A'

            image_urls = {}
            if image_url:
                image_urls['1x'] = image_url
            if image_url_2x:
                image_urls['2x'] = image_url_2x

            grocery_item = WalmartGroceryItem(
                title=title,
                product_url=response.url,
                brand=brand,
                img_url=image_urls if image_urls else 'N/A',
                price=price,
                off_price=off_price,
                product_details=product_details,
                rating=rating,
                badge=badge,
                returns_back=returns_back,
                reviews=reviews,
                keywords=[keyword.strip()
                          for keyword in keywords] if keywords else 'N/A'
            )
            yield grocery_item
        except Exception as e:
            self.logger.error(f"Error parsing product page: {e}")
