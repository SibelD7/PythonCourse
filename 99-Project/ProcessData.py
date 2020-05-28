import nltk
import os
import glob
import csv

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from string import punctuation
from numpy import array, unique

class DataProcessor(object):
    
    def __init__(self):
        nltk.download("stopwords")
        nltk.download("punkt")

        self._mSpam = []
        self._mHam = []
        self._aFeatures = []
        self._mFeatureIndex = {} # Index of every feature in the feature vector, for faster lookups
        self._aStopwords = set(stopwords.words("english"))
    
    def processSingleMail(self, sMail):
        aTokens = [ sWord.lower() for sWord in word_tokenize(sMail) ]
        aTokens = [ sWord for sWord in aTokens if sWord not in self._aStopwords ]
        aTokens = [ sWord for sWord in aTokens if sWord not in punctuation ]
        aCounts = unique(aTokens, return_counts = True)
        return dict(zip(aCounts[0], aCounts[1]))
    
    def processFile(self, sFileName, aCategoryData):
        with open(sFileName, encoding = "latin-1") as oFile:
            sData = oFile.read()
            mFeatures = self.processSingleMail(sData)
            aCategoryData.append(mFeatures)
    
    def processAllMails(self, sMailDir):
        for sFile in glob.iglob(os.path.join(sMailDir, "spam", "*.txt")):
            self.processFile(sFile, self._mSpam)
        for sFile in glob.iglob(os.path.join(sMailDir, "ham", "*.txt")):
            self.processFile(sFile, self._mHam)
    
    def buildFeatureVector(self):
        aFeatures = set()
        for sMail in self._mSpam:
            for sFeature in sMail.keys():
                aFeatures.add(sFeature)
        for sMail in self._mHam:
            for sFeature in sMail.keys():
                aFeatures.add(sFeature)
        self._aFeatures = list(aFeatures)
        for iIndex in range(0, len(self._aFeatures)):
            self._mFeatureIndex[self._aFeatures[iIndex]] = iIndex
    
    def saveFeatureVector(self, sFileName):
        with open(sFileName, "w") as oFile:
            for sWord in self._aFeatures:
                print(sWord, file = oFile)

    def loadFeatureVector(self, sFileName):
        self._aFeatures = []
        self._mFeatureIndex = {}
        with open(sFileName, "r") as oFile:
            for sWord in oFile.readlines():
                self._aFeatures.append(sWord.strip())
        for iIndex in range(0, len(self._aFeatures)):
            self._mFeatureIndex[self._aFeatures[iIndex]] = iIndex
    
    def buildMailVector(self, mMailFeatures, bIgnoreMissingFeatures = False):
        aMailVector = [0] * len(self._aFeatures)
        for sFeature, iCount in mMailFeatures.items():
            try:
                iFeatureIndex = self._mFeatureIndex[sFeature]
            except KeyError:
                if bIgnoreMissingFeatures:
                    continue
                raise
            aMailVector[iFeatureIndex] = iCount
        return aMailVector

    def buildFeatureMatrix(self, sSpamFilename, sHamFilename):
        with open(sSpamFilename, "w", newline = "") as oSpamFile:
            oSpamWriter = csv.writer(oSpamFile)
            for mMail in self._mSpam:
                oSpamWriter.writerow(self.buildMailVector(mMail))
        with open(sHamFilename, "w", newline = "") as oHamFile:
            oHamWriter = csv.writer(oHamFile)
            for mMail in self._mHam:
                oHamWriter.writerow(self.buildMailVector(mMail))
    
    def buildAdhocMailVector(self, sMailData):
        mFeatures = self.processSingleMail(sMailData)
        return array([self.buildMailVector(mFeatures, True)])
