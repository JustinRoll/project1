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
    
    #get a valid restaurant 
    def getValidRestaurant(self, **kwargs):
        response = self.search(**kwargs)
        nameMatch = False
        result = None 
        i = 0
        while not nameMatch and i < 3:
            business = response["businesses"][i]
            if business["name"].lower() == kwargs["term"].lower():
                nameMatch = True
                result = business
            i+=1
        return result
    
    def getFeatures(self, restaurantName, location):
        featureDict = {}
        yelpRestaurant = self.getValidRestaurant(term = restaurantName, location = location, limit = 3)
        if yelpRestaurant:
            featureDict["rating"] = self.getRating(yelpRestaurant)
            featureDict["reviewCount"] = self.getReviews(yelpRestaurant)
        return featureDict

    def getReviews(self, restaurant):
        reviewCount = restaurant["review_count"]
        

        if reviewCount >= 500:
            reviewCountBucket = "above500"
        elif reviewCount >= 400:
            reviewCountBucket = "above400"
        elif reviewCount >= 300:
            reviewCountBucket = "above300"
        elif reviewCount >= 200:
            reviewCountBucket = "above200"
        elif reviewCount >= 100:
            reviewCountBucket = "above100"
        else:
            reviewCountBucket = "below100"
    
        return reviewCountBucket
    
    def getRating(self, restaurant):
        rating = restaurant["rating"]

        if rating >= 4.5:
            ratingBucket = "above4.5"

        elif rating >= 4:
            ratingBucker = "above4"

        elif rating >= 3.5:
            ratingBucket = "above3.5"

        elif rating >= 3.0:
            ratingBucket = "above3"

        elif rating >= 2.0:
            ratingBucket = "above2"

        elif rating >= 1.0:
            ratingBucket = "above1"
        else:
            ratingBucket = "below1"

        return ratingBucket 
