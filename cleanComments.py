# cleanComments.py
# Author: Dimitrios Economou
#
# Takes a list of comment objects and removes unnecessary properties.
# Write result into a new file.
# Usage: python cleanComments.py <'filename'>

import sys
import json
import codecs
import csv

def cleanComments(filename):
    subreddits = "data/subreddits.csv"

    # Get {"subreddit":type} for filtering comments by subreddit
    # and adding subreddit type field to json data
    subTypes = {}
    with open(subreddits, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            subTypes[row[1]] = row[2]
    subsWeWant = subTypes.keys()

    propsToRemove = [
            'author_flair_text',
            'archived',
            'controversiality',
            'author_flair_css_class',
            'retrieved_on',
            'edited',
            'id',
            'score_hidden',
            'gilded',
            'distinguished',
            'ups',
            'downs'
    ]

    with open(filename, 'r') as infile:
        with codecs.open('_{}'.format(filename), 'w', encoding='utf-8') as outfile:
            for comment in infile:
                decodedComment = json.loads(comment)
                if decodedComment["subreddit"] not in subsWeWant:
                    continue
                if decodedComment["author"] == "[deleted]":
                    continue
                if decodedComment["body"] == "[deleted]":
                    continue
                for prop in propsToRemove:
                    # use pop to avoid exception handling
                    decodedComment.pop(prop, None)
                subreddit = decodedComment["subreddit"]
                decodedComment["sub_type"] = subTypes[subreddit]
                # Note:
                # sort_keys = True, indent = 4 gives a nice looking output
                # However, we want a comment per line.
                json.dump(decodedComment, outfile, ensure_ascii = False)
                outfile.write('\n')
        
def main(argv):
    filename = argv[0]
    cleanComments(filename)
    #fnames = ["RC_2014-09", "RC_2014-10", "RC_2014-11", "RC_2014-12", "RC_2015-01"]
    #for fname in fnames:
    #    cleanComments(fname)

if __name__ == "__main__":
    main(sys.argv[1:])
