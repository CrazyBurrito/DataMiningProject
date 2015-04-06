import glob
import os
import errno
import sys
import re

import pandas as pd
import json
import dill
import csv
import collections as cols
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

import matplotlib.pyplot as plt

def makePath(path):
    ''' Make a path with the given name if it doesn't exist. '''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def getDicts(fname, lvl=0):
    ''' Takes a file where each line is a document represented in json.
        Puts data in dictionary of dictionaries
            subWordFreq : {subreddit:{word:count}}
            ldacDict : {subreddit:{submission:{comment:{word:count}}}} 
        If lvl = 0, return subWordFreq.
        If lvl = 1, return ldacDict.
        If lvl = 2, return both of above. '''

    stopWords = set(stopwords.words('english'))
    moreStopWords = ["gt"]
    for word in moreStopWords:
        stopWords.add(word)

    minWordLen = 4
    maxWordLen = 20

    with open(fname, 'r') as infile:
        if lvl not in [0,1,2]:
            print "0: subWordFreq, 1: ldacDict, 2: both"
            return False
        subWordFreq = cols.defaultdict(lambda : cols.Counter())
        ldacDict = cols.defaultdict(lambda :
                cols.defaultdict(lambda :
                    cols.defaultdict(lambda :
                        cols.Counter())))
        stemmer = SnowballStemmer('english')
        for comment in infile:
            decodedComment = json.loads(comment)
            name = decodedComment['name'].encode('ascii', 'ignore')
            linkId = decodedComment['link_id'].encode('ascii', 'ignore')
            subreddit = decodedComment['subreddit'].encode('ascii', 'ignore')
            body = decodedComment['body'].encode('ascii', 'ignore').lower()
            bodyWordList = body.split()
            for word in bodyWordList:
                word = word.translate(string.maketrans("",""),
                        string.punctuation)
                word = stemmer.stem(word)
                if word not in stopWords and minWordLen <= len(word) <= maxWordLen and re.search('[a-z]', word):
                    if lvl == 0:
                        subWordFreq[subreddit][word] += 1
                    elif lvl == 1:
                        ldacDict[subreddit][linkId][name][word] += 1
                    else:
                        ldacDict[subreddit][linkId][name][word] += 1
                        subWordFreq[subreddit][word] += 1
        if lvl == 0:
            return subWordFreq
        if lvl == 1:
            return ldacDict
        else:
            return subWordFreq, ldacDict

def dictToFiles(ldacDict):
    minComments = 10
    for subreddit in ldacDict.keys():
        for linkId in ldacDict[subreddit].keys():
            if len(ldacDict[subreddit][linkId].keys()) < minComments:
                # require submission to have at least minComments
                continue
            makePath("ldacCom/{0}".format(subreddit))
            for name in ldacDict[subreddit][linkId].keys():
                totalWordCount = sum(ldacDict[subreddit][linkId][name].values())
                line = str(totalWordCount) + "".join(" " + word + ":" +
                    str(ldacDict[subreddit][linkId][name][word]) for word in
                    ldacDict[subreddit][linkId][name].keys())
                line += '\n'
                with open("ldacCom/{0}/{1}".format(subreddit,linkId), 'a') as outfile:
                    outfile.write(line)

def myTokenizer(doc):
    ''' Takes a document and and returns a list of the document's
        tokens. May use this to get tfidf matrices later. '''
    # Need a stemmer instance to get word stems.
    stemmer = SnowballStemmer("english")
    # Tokenize by sentence, then by word.
    tokens = [word.lower() for sent in nltk.sent_tokenize(doc)
            for word in nltk.word_tokenize(sent)]
    # Filter tokens.
    minLen = 4
    maxLen = 20
    filteredTokens = []
    for token in tokens:
        if re.search('[a-z]', token) and minLen <= len(token) <= maxLen:
            filteredTokens.append(stemmer.stem(token))
    return filteredTokens

# from redditanalytics json data, get convenient dictionaries storing
# subreddit word counts and a dictionary representing Blei's LDA-C format
def main():
    fname = "data/testdata"
    dictOnDisk = 'swf'
    saveSubWordFreq = True
    saveLdacDict = True
    
    # for testing purposes, get subreddits with at least n words
    needDict = False
    if needDict:
        subWordFreq = getDicts(fname)
        n = 50
        for subreddit in subWordFreq.keys():
            if len(subWordFreq[subreddit].keys()) < n:
                subWordFreq.pop(subreddit, None)
        if saveSubWordFreq:
            print "Saving dictionary to disk."
            dill.dump(subWordFreq, open('subWordFreq', 'w'))
    else:
        with open('swf','r') as infile:
            swf = dill.load(infile)

    # make term-document matrix
    allWords = set()
    for doc in swf.keys():
        for word in swf[doc].keys():
            allWords.add(word)
    allWords = list(allWords)
    allDocs = range(len(swf.keys()))
    wordDictionary = {}
    for index, word in enumerate(allWords):
        wordDictionary[word] = index

    # convert to sparse matrix
    from scipy.sparse import csr_matrix, dok_matrix
    subreddits = swf.keys()
    sparseDokMatrix = dok_matrix((len(subreddits), len(allWords)), dtype=np.int32)
    for subreddit in subreddits:
        subIndex = subreddits.index(subreddit)
        for word in swf[subreddit].keys():
            wordIndex = wordDictionary[word]
            sparseDokMatrix[subIndex, wordIndex] = swf[subreddit][word]

    tfidfTransformer = TfidfTransformer()
    tfidfMatrix = tfidfTransformer.fit_transform(sparseDokMatrix)

    # Now that we have the tfidf matrix, we can start clustering subreddits.
    # First let our distance metric be cosine
    from sklearn.metrics.pairwise import cosine_similarity
    dist = 1 - cosine_similarity(tfidfMatrix)

    # Let's try k-means clustering
    from sklearn.cluster import KMeans
    nClusters = 30
    km = KMeans(n_clusters=nClusters)
    km.fit(tfidfMatrix)
    clusters = km.labels_.tolist()
    # To save and load the model:
    #from sklearn.externals import joblib
    #joblib.dump(km,  'doc_cluster.pkl')
    #km = joblib.load('doc_cluster.pkl')

    # print results
    from itertools import groupby
    subClus = zip(clusters, subreddits)
    #subclus = sorted(subClus, key=lambda x: x[0])
    for key, group in groupby(sorted(subClus,key=lambda x: x[0]), lambda x: x[0]):
        aGroup = ", ".join(["%s" % thing[1] for thing in group])
        print str(key) + ":    " + aGroup
        print

    # Ward hierarchical clustering
    from scipy.cluster.hierarchy import ward, dendrogram
    linkageMatrix = ward(dist)

    fig, ax = plt.subplots(figsize=(8,60))
    ax = dendrogram(linkageMatrix, orientation='right', labels=subreddits)
    plt.tick_params(\
        axis= 'x',
        which='both',
        bottom='off',
        top='off',
        labelbottom='off')
    plt.tight_layout()
    plt.savefig('ward-cosine.png', dpi=200)
        

if __name__ == "__main__":
    main()
