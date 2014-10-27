import random,operator,nltk
import functools
from nltk.corpus import udhr
from nltk import bigrams
from nltk.tokenize import word_tokenize, sent_tokenize 
from nltk.corpus import stopwords

class DocumentFeature:
    
    def tokenize(self, doc):
        tokenizedDoc = [word.lower() if not word in stopwords.words('english') for sent in sent_tokenize(bustaSoup.get_text()) for word in word_tokenize(sent)]
        return tokenizedDoc
    
    def docFeatures(self, doc):
        featureDict = {}

        tokenizedDoc = self.tokenize(doc)
        stringBigrams = bigrams(doc)
        for bg in stringBigrams:
            featureDict[bg] = True

        for word in tokenizedDoc:
            featureDict[word] = True

        return tokenizedDoc

