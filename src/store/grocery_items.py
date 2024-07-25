import scrapy


class WalmartGroceryItem(scrapy.Item):
    # define the fields for your item here like:
    # name
    title = scrapy.Field()
    product_url = scrapy.Field()
    brand = scrapy.Field()
    img_url = scrapy.Field()
    price = scrapy.Field()
    off_price = scrapy.Field()
    product_details = scrapy.Field()
    rating = scrapy.Field()
    badge = scrapy.Field()
    returns_back = scrapy.Field()
    reviews = scrapy.Field()
    keywords = scrapy.Field()
