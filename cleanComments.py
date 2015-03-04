# cleanComments.py
# Author: Dimitrios Economou
#
# Takes a list of comment objects and removes unnecessary properties. Write result into a new file.
# Usage: python cleanComments.py <'filename'>

import sys
import json
import codecs

def cleanComments(filename):
    propsToRemove = [
            'author_flair_text',
            'archived',
            'controversiality',
            'author_flair_css_class',
            'retrieved_on',
            'edited',
            'id',
            'score_hidden',
            'gilded'
    ]

    with open(filename, 'r') as infile:
        with codecs.open('_{}'.format(filename), 'w', encoding='utf-8') as outfile:
            for comment in infile:
                decodedComment = json.loads(comment)
                for prop in propsToRemove:
                    # use pop to avoid exception handling
                    decodedComment.pop(prop, None)
                # Note:
                # sort_keys = True, indent = 4 gives a nice looking output
                # However, we want a comment per line.
                json.dump(decodedComment, outfile, ensure_ascii = False)
                outfile.write('\n')
        
def main(argv):
    filename = argv[0]
    cleanComments(filename)

if __name__ == "__main__":
    main(sys.argv[1:])
