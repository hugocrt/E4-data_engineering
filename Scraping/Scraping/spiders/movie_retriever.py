"""
Authors : CARANGEOT Hugo, CONTE-DEVOLX Titouan
Produced : January 2024
⚠ FREE TO USE FOR PERSONAL USE ⚠

Module Docstring:
This module contains a Scrapy spider for scraping movie data from the SensCritique website.
"""

import scrapy
from scrapy.http import Request
from ..items import ArticleItem


class MySpider(scrapy.Spider):
    """
    Class Docstring:
    MySpider is a Scrapy spider designed to crawl SensCritique and retrieve information about
    movies.

    Attributes:
    - name (str): The name of the spider.
    - allowed_domains (list): List of allowed domains for crawling.
    - start_urls (list): List of starting URLs for the spider.

    Methods:
    - parse(response, **kwargs): Parse method to extract movie rankings and initiate requests
    for detailed information.
    - parse_movie(response): Parse method to extract detailed information about a movie.
    """

    name = "senscritique"
    allowed_domains = ["senscritique.com"]
    start_urls = [f"https://www.senscritique.com/liste/les_1000_plus_grands_"
                  f"films_de_tous_les_temps_they_shoot_pict/2794779?page={i}"
                  for i in range(1, 35)]

    def parse(self, response, **kwargs):
        """
        Method Docstring:
        Parse method for extracting movie rankings and initiating requests for detailed information.

        Args:
        - response (scrapy.http.Response): The response object from the crawled page.
        - **kwargs: Additional keyword arguments.

        Yields:
        - scrapy.http.Request: Requests for detailed information about each movie.
        """

        for movie_block in response.css('.bPTEEs'):
            # Extract ranking as a string containing digits only
            ranking = ''.join(filter(str.isdigit, movie_block.css('span::text').get()))
            movie_link = movie_block.css('a::attr(href)').get()

            yield Request(
                url=response.urljoin(movie_link),
                callback=self.parse_movie,
                meta={'ranking': ranking}
            )

    @staticmethod
    def parse_movie(response):
        """
        Method Docstring:
        Parse method for extracting detailed information about a movie.

        Args:
        - response (scrapy.http.Response): The response object from the crawled page.

        Yields:
        - items.ArticleItem: Item containing detailed information about a movie.
        """

        movie_info = response.css("p[data-testid='creators']")

        yield ArticleItem(
            title=response.css("h1::text").get(),
            ranking=response.meta.get('ranking'),
            genres=response.css(".dnsVaH a[href^='/films/']::text").extract(),
            director=movie_info.css("a[data-testid='link'] span::text").get(),
            duration=movie_info.re_first(r"· (\d+ h \d+ min)"),
            publication_year=response.css(".cuIThM::text").get(),
            poster=response.css("[data-testid='poster-img']::attr(src)").get(),
            native_countries=response.css(".dnsVaH span:not([class])::text").get()
        )
