# -*- coding: utf-8 -*-

import scrapy
import pycountry
import uuid
from locations.categories import Code
from locations.items import GeojsonPointItem

class KrispyKremeSpider(scrapy.Spider):
    
    name = "krispy_kreme_tur_dpa"
    brand_name = "Krispy Kreme"
    spider_type = "chain"
    spider_chain_id = "1844"
    spider_categories = [
        Code.DOUGHNUT_SHOP.value
    ]
    spider_countries = [
        pycountry.countries.lookup("TUR").alpha_3
    ]

    start_urls = ["https://www.krispykreme.com.tr/magaza"]

    def parse(self, response):
        # Extract the <ul> with class 'list-unstyled'
        ul_element = response.css('ul.list-unstyled')

        for li in ul_element.css('li'):
            title = li.css('h5::text').get().strip()
            address = li.css('p::text').get().strip()
            phone = li.css('p.phone::text').get()
            phone = li.css('p.phone::text').get()
            if phone:
                phone = phone.replace('T:', '').strip()

            latitude = li.attrib.get('data-map-yatay', '')
            longitude = li.attrib.get('data-map-dikey', '')

            mappedAttributes = {
                'chain_name': self.brand_name,
                'chain_id': self.spider_chain_id,
                'ref': uuid.uuid4().hex,
                'addr_full': address,
                'phone': phone,
                'website': response.url,
                'lat': latitude,
                'lon': longitude,
            }

            yield GeojsonPointItem(**mappedAttributes)
