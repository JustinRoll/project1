import re
from bs4 import BeautifulSoup
import glob, os
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
        self.ratingParagraphMap = {}
    def get_dict(self):
        return {"reviewer" : self.reviewer, "name" : self.name, "city" : self.city,
                "food" : self.food, "service" : self.service, "venue" : self.venue,
                "rating" : self.rating, "paragraphs" : self.paragraphs}
    #food service venue
    def make_paragraph_map(self):
        if len(self.paragraphs) >= 4:
            self.ratingParagraphMap[self.food] = self.paragraphs[0]
            self.ratingParagraphMap[self.service] = self.paragraphs[1]
            self.ratingParagraphMap[self.venue] = self.paragraphs[2]

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
    html = re.sub(r"\<span[^>]*>", " ", html)
    html = re.sub(r"\<\/span>", " ", html)
    html = re.sub(r"<br \/>", "</p><p>", html)
    soup = BeautifulSoup(html)
    paragraphs = soup.find_all('p')
    reviews = []
    review = None
    pMode = False
    metaMode = False
    for paragraph in paragraphs:
        contents = [x if isinstance(x, str) else "\n" for x in paragraph.contents]
        plaintext = "\n".join(contents)
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
    review.make_paragraph_map()
    reviews.append(review)
    return reviews

def importReviews(directory):
    reviews = []
    for filename in glob.glob(os.path.join(directory, '*.html')):
        f = open(filename, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        newRevs = parseReview(content)
        reviews.extend(newRevs)
        for rev in newRevs:
            if len(rev.paragraphs) != 4:
                print(filename)
                print(len(rev.paragraphs))
                #prints names of files that were not correctly parsed
    return reviews

importReviews("./reviews")
