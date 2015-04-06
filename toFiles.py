# toFiles.py
# Author: Dimitrios Economou
#
# Puts comments into files. Probably won't use this.

import sys
import json
import codecs
import glob
import os
import errno

def makePath(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def main(argv):
    # get list of subreddits we are interested in
    with open("subreddits.list") as subredditsFile:
        subredditsWithNewLines = subredditsFile.readlines()
        subreddits = {x.strip('\n').lower() for x in subredditsWithNewLines}
        print len(subreddits)

    for f in glob.glob("_*"):
        with open(f) as fopen:
            for comment in fopen:
                decodedComment = json.loads(comment)
                subreddit = decodedComment["subreddit"]
                if subreddit.lower() not in subreddits:
                    continue
                commentId = decodedComment["name"]
                parentId = decodedComment["parent_id"]
                submissionId = decodedComment["link_id"]
                makePath("{0}/{1}".format(subreddit, submissionId))
                with codecs.open('{0}/{1}/{2}-{3}'.format(subreddit, submissionId, commentId, parentId), 'w', encoding='utf-8') as commentTxt:
                    commentTxt.write(decodedComment["body"])

if __name__ == "__main__":
    main(sys.argv[1:])
