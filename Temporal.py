# Temporal.py
# Author: Josh Weaver
#
# Takes a list of comment objects and extracts temporal changes in submission 
# popularity
# Write result into a new file.
# Usage: python Temporal.py <'filename'>

import sys
import signal
import json
import praw
import datetime
import matplotlib
import pylab
import codecs
import urllib2
import requests

def signal_handler(signal, frame):
    #sys.exit(0)
    for i in range(len(time)):
        commentsByHour[int(time[i][11:13])].append(comments[i])
        
    for i in range(len(commentsByHour)):
        sum1 = 0
        for j in range(len(commentsByHour[i])):
            sum1 += commentsByHour[i][j]
        if len(commentsByHour[i]) is not 0:
            avg.append(sum1/len(commentsByHour[i]))
        else:  
            avg.append(0)
        
        
    matplotlib.pyplot.xlabel("Hour")
    matplotlib.pyplot.ylabel("Average Number of Comments")
    matplotlib.pyplot.xlim(xmin=0)
    matplotlib.pyplot.xlim(xmax=24)
    matplotlib.pyplot.bar(range(24),avg)

    matplotlib.pyplot.show()   

signal.signal(signal.SIGINT, signal_handler)

#def main(argv):
filename = sys.argv[1:][0]


#fnames = ["RC_2014-09", "RC_2014-10", "RC_2014-11", "RC_2014-12", "RC_2015-01"]
#for fname in fnames:
#    cleanComments(fname)
r = praw.Reddit('Temporal submission data collection by /u/jay501')

commentsByHour = [[] for j in range(24)]
time = list()
comments = list()
subs = list()
avg = list()

with open(filename, 'r') as infile:
    for comment in infile:
        try:
            decodedComment = json.loads(comment)
            subs.append(decodedComment.pop('link_id', None)[3:])
        except: continue

#subs = {"34aeeu", "34a7cw", "34afpx", "34afpx","349fmy","347xl8","349hzp","347lp2","348v1o","34a7cw","349e6g"}
submissions = list(set(subs)) 
#try:
for i in range(len(submissions)):
    print ("Grabbing submission ",i)
    try:
        submission = r.get_submission(submission_id = submissions[i])
        
    except requests.exceptions.HTTPError:
        print ("here")
        continue
    vars1 = vars(submission)
    rawtime = vars1['created_utc']
    time.append( datetime.datetime.fromtimestamp(rawtime).strftime('%m/%d/%Y %H:%M:%S'))
    comments.append(vars1['num_comments'])
#except KeyboardInterrupt:
    #sys.exit(0)

for i in range(len(time)):
    commentsByHour[int(time[i][11:13])].append(comments[i])
    
for i in range(len(commentsByHour)):
    sum1 = 0
    for j in range(len(commentsByHour[i])):
        sum1 += commentsByHour[i][j]
    if len(commentsByHour[i]) is not 0:
        avg.append(sum1/len(commentsByHour[i]))
    else:  
        avg.append(0)
    
    
matplotlib.pyplot.xlabel("Hour")
matplotlib.pyplot.ylabel("Average Number of Comments")
matplotlib.pyplot.xlim(xmin=0)
matplotlib.pyplot.xlim(xmax=24)
matplotlib.pyplot.bar(range(24),avg)

matplotlib.pyplot.show()    
    
