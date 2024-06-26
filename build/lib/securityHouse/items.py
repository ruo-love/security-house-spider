# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SecurityhouseItem(scrapy.Item):
    # define the fields for your item here like:
    types = scrapy.Field()
    max = scrapy.Field()
    title = scrapy.Field()
    key = scrapy.Field()
    area = scrapy.Field()
    years = scrapy.Field()
    link = scrapy.Field()
    local = scrapy.Field()
    approved_value = scrapy.Field()  # 本批准予
    participated_value = scrapy.Field()  # 参与
    selected_value = scrapy.Field()  # 选购
    one = scrapy.Field()  # 一居室
    two = scrapy.Field()  # 二居室
    three = scrapy.Field()  # 三居室
    total = scrapy.Field()  # total
    pass
