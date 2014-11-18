from yelpQuery import YelpQuery
from classifier import Classifier
from review import *

def main():
    reviews = importReviews("./reviews")
    classifier = Classifier(reviews)

    print("Overall Score Average accuracy: %f" % (classifier.getAverages(classifier.classifyOverallReviews)[1]))
    print("Overall Score Exact rmse: %f, accuracy: %f" % (classifier.getAverages(classifier.classifyOverallReviewsExact)))
    print("Paragraph accuracy: %f" % (classifier.getAverages(classifier.classifyParagraphReviews)[1]))
    print("Paragraph Exact Score rmse: %f, accuracy: %f" % (classifier.getAverages(classifier.classifyParagraphReviewsExact)))
    print("Authorship rmse: %f, accuracy: %f" % (classifier.getAverages(classifier.classifyAuthorshipReviews)))
#    print("Exact Score (0-5) Paragraph rmse: %f, accuracy: %f" % (classifier.classifyParagraphReviewsExact()))
#    print("Overall rmse: %f, accuracy: %f" % (classifier.classifyOverallReviews()))
#    print("Exact Overall rmse: %f, accuracy: %f" % (classifier.classifyOverallReviewsExact()))
#    print("Authorship score: %f" % classifier.classifyAuthorshipReviews())
main() 
