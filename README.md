# Web Scraper Project

## Overview

This project is a comprehensive web scraper built using Python and Scrapy. It allows you to extract data from websites in a structured manner, making it easy to gather information for various purposes.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/royalihasan/comprehensive-web-scraper-using-python-and-scrapy.git
    cd comprehensive-web-scraper-using-python-and-scrapy
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
## ScrapeOps Integration Guide
> Why we need this?

Because ScrapeOps provides a proxy service that allows you to scrape websites at scale without getting blocked. By integrating ScrapeOps with your Scrapy project, you can easily rotate IP addresses and avoid getting blocked by websites.
  

### Step 1: Create an Account on ScrapeOps
1. Visit the [ScrapeOps website](https://scrapeops.io/).
2. Sign up for an account using your email address.
3. Once your account is created, log in to your ScrapeOps dashboard.

### Step 2: Obtain Your API Key
1. Navigate to the API section of the ScrapeOps dashboard.
2. Copy your unique API key provided by ScrapeOps.

### Step 3: Add ScrapeOps API Key to Your Scrapy Project
1. Open the `src/settings.py` file in your Scrapy project.
2. Add the following configuration to include your ScrapeOps API key:

```python
SCRAPEOPS_API_KEY = 'your_scrapeops_api_key_here'

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.ScrapeOpsProxyMiddleware': 725,
    # other middlewares
}
SCRAPEOPS_PROXY_ENABLED = True
```


## Configuration

The main configuration settings for the Scrapy project are located in `src/settings.py`. Key settings include:

- `BOT_NAME`: The name of the bot.
- `SPIDER_MODULES`: The modules where spiders are located.
- `NEWSPIDER_MODULE`: The module for new spiders.
- `ROBOTSTXT_OBEY`: Whether to obey robots.txt rules.
- `ITEM_PIPELINES`: Pipelines for processing scraped items.
- `DOWNLOADER_MIDDLEWARES`: Middlewares for processing requests and responses.


## Usage

1. To run the scraper, use the following command:
    ```sh
    scrapy crawl <spider_name>
    ```

2. The scraped data will be saved in `items.json` by default, as configured in the `JsonWriterPipeline` class in `src/pipelines.py`.


