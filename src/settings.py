

BOT_NAME = "web_scraper"

SPIDER_MODULES = ["src.spiders"]
NEWSPIDER_MODULE = "src.spiders"



ROBOTSTXT_OBEY = False


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    'src.pipelines.JsonWriterPipeline': 1, 
}


# 


SCRAPEOPS_API_KEY = '9bdfd7a6-5eed-4b80-938a-1bf645f2a1fc'


SCRAPEOPS_PROXY_ENABLED = True
CONCURRENT_REQUESTS = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}
