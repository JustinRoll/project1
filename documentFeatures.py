import random,operator,nltk
import functools
from nltk.corpus import udhr
from nltk import bigrams
from nltk.tokenize import word_tokenize, sent_tokenize 
from nltk.corpus import stopwords, wordnet
from nltk.stem.porter import PorterStemmer

class DocumentFeature:
    
    def tokenize(self, doc):
        stemmer = PorterStemmer()
        tokenizedDoc = [word.lower() for sent in sent_tokenize(doc) for word in word_tokenize(sent)]
        stemmedDoc = map(stemmer.stem, tokenizedDoc)
        return tokenizedDoc, stemmedDoc
    
    def docFeatures(self, doc):
        featureDict = {}

        tokenizedDoc = self.tokenize(doc)
        stringBigrams = bigrams(doc)
        for bg in stringBigrams:
            featureDict[bg] = True

        for word in tokenizedDoc:
            featureDict[word] = True

        return featureDict

    def compareSynsets(self, word):
        posSynsets = wordnet.synsets("positive")
        negSynsets = wordnet.synsets("negative")
        wordSynsets = wordnet.synsets(word)
        
        print(wordSynsets[0].path_similarity(posSynsets[0]))
        print(wordSynsets[0].path_similarity(negSynsets[0]))
               
