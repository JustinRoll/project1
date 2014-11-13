from yelpQuery import YelpQuery
from classifier import Classifier
from review import *

def main():
    reviews = importReviews("./reviews")
    classifier = Classifier(reviews)
    print(classifier.classifyAuthorshipReviews())
    print(classifier.classifyOverallReviews())
    print(classifier.classifyParagraphReviews())
main() 
