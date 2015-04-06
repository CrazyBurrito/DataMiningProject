import json
import sqlite3
import sys

def main(argv):
    if len(argv) != 2:
        sys.exit("Provide a comment file (of json objects) name.")

    fname = argv[1]
   
    db = sqlite3.connect("testdb")
    columns = ['name', 'author', 'body', 'score', 'parent_id', 'link_id', 'subreddit', 'subreddit_id', 'sub_type', 'created_utc']

    query = "insert or ignore into Comments values (?,?,?,?,?,?,?,?,?,?)"

    c = db.cursor()

    with open(fname, 'r') as infile:
        for comment in infile:
            decodedComment = json.loads(comment)
            keys = [decodedComment[col] for col in columns]
            print str(keys)
            print
            c.execute(query, keys)

    c.close()
    db.commit()
    db.close()

    
if __name__ == "__main__":
    main(sys.argv)
