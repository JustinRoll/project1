import argparse
import json
import pprint
import sys
import urllib
from yelpapi import YelpAPI




class YelpQuery:

    def __init__(self):
        self.DEFAULT_TERM = 'dinner'
        self.DEFAULT_LOCATION = 'San Luis Obispo, CA'
        self.SEARCH_LIMIT = 3
        self.SEARCH_PATH = '/v2/search/'
        self.BUSINESS_PATH = '/v2/business/'

        self.CONSUMER_KEY = "0Ji9mpDmiH0rub9AvjtRhQ"
        self.CONSUMER_SECRET = "b7SZdC5XVqbo3SKvlK28bs12hrM"
        self.TOKEN = "DTNxH_G-2dF_PmiZzY7geQJnW5rcVWxu"
        self.TOKEN_SECRET = "dj-jziXREJcEf3vtmwWkqQFXu_8" 

    def connect(self):
        self.yelp_api = YelpAPI(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.TOKEN, self.TOKEN_SECRET)

    def get_business(self, business_id, **kw_args):
        business_results = self.yelp_api.business_query(id=business_id, **kw_args)
        return businessResults

    def search(self, **kwargs):
        search_results = self.yelp_api.search_query(**kwargs)
        return search_results
