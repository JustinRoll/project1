from yelpQuery import YelpQuery
from classifier import Classifier
from review import *

def main():
    reviews = importReviews("./reviews")
    classifier = Classifier(reviews)
    #print(classifier.classifyOverallReviews())
    #print(classifier.classifyOverallReviewsExact())
    #print(classifier.classifyParagraphReviews())
    #print(classifier.classifyParagraphReviewsExact())
    print(classifier.classifyAuthorshipReviews())
main() 
