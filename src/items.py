import scrapy

class WalmartItem(scrapy.Item):
    keyword = scrapy.Field()
    page = scrapy.Field()
    position = scrapy.Field()
    id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    averageRating = scrapy.Field()
    manufacturerName = scrapy.Field()
    shortDescription = scrapy.Field()
    thumbnailUrl = scrapy.Field()
    price = scrapy.Field()
    currencyUnit = scrapy.Field()
