# cleanSubs.py
# Author: Dimitrios Economou
#
# This was used to clean the file containing the subreddits we want.
# It removes duplicates and columns we don't want.

import sys
import json
import codecs
import csv

def cleanSubs(filename):
    with open('subreddits.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        industry = []
        subreddit = []
        subType = []
        for row in csvreader:
            industry.append(row[0].lower())
            subreddit.append(row[1].lower())
            subType.append(row[3].lower())
        rows = zip(industry, subreddit, subType)
        # for removing duplicates
        subreddits = set()
        with open('cleanedSubs.csv', 'wb') as outcsvfile:
            csvwriter = csv.writer(outcsvfile)
            for row in rows:
                if row[1] not in subreddits:
                    csvwriter.writerow(row)
                    subreddits.add(row[1])
        
def main():
    filename = "subreddits.csv"
    cleanSubs(filename)

if __name__ == "__main__":
    main()
