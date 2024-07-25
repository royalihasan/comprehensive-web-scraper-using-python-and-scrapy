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

# AGENT SETTINGS
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


# Playwright settings
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     "headless": False

# }
# PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 100000

# SCRAPEOPS SETTINGS

SCRAPEOPS_API_KEY = '4f5dc63e-2a51-4420-98f7-4fd60db6e79f'
SCRAPEOPS_PROXY_ENABLED = True
CONCURRENT_REQUESTS = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}
