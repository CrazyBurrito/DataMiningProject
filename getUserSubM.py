import sys
import json
import shelve
import csv

def main():
    # initialize data structures and set variables
    fname = "data/2014-10-cleaned"
    users = {}
    subreddits = set()
    subCount = {}
    # thresholds
    userSubT = 2                # min number of subreddits user must comment to
    userCommentsT = 5          # min number of comments user must have made
    nSubT = 10                 # min number times sub commented in

    # put data in dictionary of dictionaries {user:{sub:count}}
    with open(fname, 'r') as infile:
        for comment in infile:
            decodedComment = json.loads(comment)
            subreddit = decodedComment['subreddit'].encode('ascii', 'ignore')
            subreddits.add(subreddit)
            author = decodedComment['author'].encode('ascii', 'ignore')
            if author not in users:
                users[author] = {subreddit: 0}
            if subreddit not in users[author]:
                users[author][subreddit] = 0
            users[author][subreddit] += 1

    # reduce data based on thresholds
    for subreddit in subreddits:
        subCount[subreddit] = 0
    for user in users.keys():
        if len(users[user].keys()) < userSubT:
            users.pop(user, None)
            continue
        if sum(users[user].values()) < userCommentsT:
            users.pop(user, None)
            continue
        for subreddit in users[user].keys():
            subCount[subreddit] += users[user][subreddit]
    subreddits = [x for x in subreddits if subCount[subreddit] >= nSubT]

    # myShelve = shelve.open('userSub.shelve')
    # myShelve.update(users)
    # myShelve.close()
    
    # output reduced dictionary to csv for analysis
    w = csv.writer(open("userSub.csv", 'w'))
    # write top row of subreddits
    w.writerow(subreddits)
    for user in users.keys():
        row = []
        for subreddit in subreddits:
            if subreddit not in users[user].keys():
                row.append(0)
            else:
                row.append(users[user][subreddit])
        w.writerow(row)

if __name__ == "__main__":
    main()
