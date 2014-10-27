import re
from bs4 import BeautifulSoup
class Review:
    def __init__(self):
        self.reviewer = ""
        self.name = ""
        self.address = ""
        self.city = ""
        self.food = 0
        self.service = 0
        self.venue = 0
        self.rating = 0
        self.paragraphs = list()

    def get_dict(self):
        return {"reviewer" : self.reviewer, "name" : self.name, "city" : self.city,
                "food" : self.food, "service" : self.service, "venue" : self.venue,
                "rating" : self.rating, "paragraphs" : self.paragraphs}

tagRegex = r'\<[^>]*\>'
reviewerRegex = r'REVIEWER:\s*(.*)'
nameRegex = r'NAME:\s*(.*)'
addressRegex = r'ADDRESS:\s*(.*)'
cityRegex = r'CITY:\s*(.*)'
foodRegex = r'FOOD:\s*(\d)'
serviceRegex = r'SERVICE:\s*(\d)'
venueRegex = r'VENUE:\s*(\d)'
ratingRegex = r'RATING:\s*(.*)'
writtenReviewRegex = r'WRITTEN REVIEW:'

def parseReview(html):
    soup = BeautifulSoup(html)
    paragraphs = soup.find_all('p')
    reviews = []
    review = None
    pMode = False
    metaMode = False
    for paragraph in paragraphs:
        contents = [x if isinstance(x, str) else "\n" for x in paragraph.contents]
        plaintext = "".join(contents)
        reviewer = re.search(reviewerRegex, plaintext, re.IGNORECASE)
        name = re.search(nameRegex, plaintext, re.IGNORECASE)
        address = re.search(addressRegex, plaintext, re.IGNORECASE)
        city = re.search(cityRegex, plaintext, re.IGNORECASE)
        food = re.search(foodRegex, plaintext, re.IGNORECASE)
        service = re.search(serviceRegex, plaintext, re.IGNORECASE)
        venue = re.search(venueRegex, plaintext, re.IGNORECASE)
        rating = re.search(ratingRegex, plaintext, re.IGNORECASE)
        writtenReview = re.search(writtenReviewRegex, plaintext, re.IGNORECASE)
        if reviewer and not metaMode:
            pMode = False
            if review:
                reviews.append(review)
            review = Review()
            metaMode =True
            review.reviewer = reviewer.group(1)
        if name:
            review.name = name.group(1)
        if address:
            review.address = address.group(1)
        if city:
            review.city = city.group(1)
        if food:
            review.food = int(food.group(1))
        if service:
            review.service = int(service.group(1))
        if venue:
            review.venue = int(venue.group(1))
        if rating:
            review.rating = int(rating.group(1))
        if writtenReview:
            pMode = True
            metaMode = False
        elif pMode and len(plaintext) > 4:
            review.paragraphs.append(plaintext)
    reviews.append(review)        
    return reviews

