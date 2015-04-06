import json
import sqlite3
import sys

def main(argv):
    if len(argv) != 2:
        sys.exit("Provide a database name.")

    dbName = argv[1]
    db = sqlite3.connect(dbName)

    db.execute('''CREATE TABLE IF NOT EXISTS Comments
              (name text primary key,
               author text,
               body text,
               score integer,
               parent_id text,
               link_id text,
               subreddit text,
               subreddit_id text,
               sub_type text,
               created_utc text,
               foreign key (parent_id) references Comments(name));''')
    
    db.commit()
    db.close()
    
if __name__ == "__main__":
    main(sys.argv)
