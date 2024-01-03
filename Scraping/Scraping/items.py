# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    ranking = scrapy.Field()
    genres = scrapy.Field()
    director = scrapy.Field()
    duration = scrapy.Field()
    publication_year = scrapy.Field()
    poster = scrapy.Field()
    native_countries = scrapy.Field()




