from yelpQuery import YelpQuery
from classifier import Classifier
from review import *

def main():
    reviews = importReviews("./reviews")
    classifier = Classifier(reviews)
    print("Paragraph rmse: %f, accuracy: %f" % (classifier.classifyParagraphReviews()))
    print("Exact Score (0-5) Paragraph rmse: %f, accuracy: %f" % (classifier.classifyParagraphReviewsExact()))
    print("Overall rmse: %f, accuracy: %f" % (classifier.classifyOverallReviews()))
    print("Exact Overall rmse: %f, accuracy: %f" % (classifier.classifyOverallReviewsExact()))
    print("Authorship score: %f" % classifier.classifyAuthorshipReviews())
main() 
