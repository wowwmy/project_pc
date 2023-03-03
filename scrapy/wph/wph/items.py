# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WphItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brandShowName = scrapy.Field()
    title = scrapy.Field()
    marketPrice = scrapy.Field()
    saleDiscount = scrapy.Field()
    salePrice = scrapy.Field()
