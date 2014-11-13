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
        while not nameMatch and i < 3 and i < len(response["businesses"]):
            business = response["businesses"][i]
            if business["name"].lower() == kwargs["term"].lower():
                nameMatch = True
                result = business
            i+=1
        
        if len(response["businesses"]) > 0:
                result = response["businesses"][0]
       
        return result

    def getExactFeatures(self, restaurantName, location, weight):
        featureDict = {}
        if location == "Arnold":
                location = "Arnold, CA"
        elif restaurantName == "G-Brothers Kettlecorn":
                restaurantName = "G Brothers"
        elif location == "Shell Beach" and "intock" in restaurantName:
                restaurantName = "F. McLintocks Saloon & Dining House"
                location = "Shell Beach, CA"
        

        yelpRestaurant = self.getValidRestaurant(term = restaurantName, location = location, limit = 3)
        if yelpRestaurant:
            rating = self.getExactRating(yelpRestaurant)
            reviewCount = self.getReviews(yelpRestaurant)
        else:
            rating = self.getExactRating({"rating" : 3.0, "review_count" : 21})
            reviewCount = self.getReviews({"rating": 3.0, "review_count" : 21})
         #the only restaurant for which this failed is Alphys. Hardcoding the vals from
         #Alphys Chateau Basque at http://www.yelp.com/biz/alphys-chateau-basque-pismo-beach-2
            print("No yelp info for %s in %s" % (restaurantName, location))
         
        for i in range(1, weight + 1):
            featureDict["rating%d" %i] = rating
            featureDict["reviewCount%d" %i] = reviewCount
                
        return featureDict 

    def getFeatures(self, restaurantName, location, weight):
        featureDict = {}
        if location == "Arnold":
                location = "Arnold, CA"
        elif restaurantName == "G-Brothers Kettlecorn":
                restaurantName = "G Brothers"
        elif location == "Shell Beach" and "intock" in restaurantName:
                restaurantName = "F. McLintocks Saloon & Dining House"
                location = "Shell Beach, CA"
        

        yelpRestaurant = self.getValidRestaurant(term = restaurantName, location = location, limit = 3)
        if yelpRestaurant:
            rating = self.getRating(yelpRestaurant)
            reviewCount = self.getReviews(yelpRestaurant)
        else:
            rating = self.getRating({"rating" : 3.0, "review_count" : 21})
            reviewCount = self.getRating({"rating": 3.0, "review_count" : 21})
         #the only restaurant for which this failed is Alphys. Hardcoding the vals from
         #Alphys Chateau Basque at http://www.yelp.com/biz/alphys-chateau-basque-pismo-beach-2
            print("No yelp info for %s in %s" % (restaurantName, location))
         
        for i in range(1, weight + 1):
            featureDict["rating%d" %i] = rating
            featureDict["reviewCount%d" %i] = reviewCount
                
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

    def getExactRating(self, restaurant):
        rating = restaurant["rating"]
        ratingBucket = None

        if rating >= 4.5:
            ratingBucket = "above45"
        elif rating >= 4.0:
            ratingBucket = "above4"
        elif rating >= 3.0:
            ratingBucket = "above3"
        elif rating >= 2.0:
            ratingBucket = "above2"
        elif ratingBucket >= 1.0:
            ratingBucket = "above1"
        else:
            ratingBucket = "above0"

        return ratingBucket 

    def getRating(self, restaurant):
        rating = restaurant["rating"]
        ratingBucket = None

        if rating >= 4.0:
            ratingBucket = "positive"

        else:
            ratingBucket = "negative"

        return ratingBucket 
