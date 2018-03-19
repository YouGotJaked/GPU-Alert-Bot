import praw
import config
import time
import os
import sys

my_file = "log.txt"

# log into reddit using config.py
def login():
    print "Logging in..."
    
    reddit = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "GPU Alert Bot")
    
    print "Logged in!"
            
    return reddit

# searches for a target word in a specific subreddit and prints out the count
def run_bot(reddit,target,sub,lim,secs):
    subreddit = reddit.subreddit(sub)
    
    for submission in subreddit.new(limit = lim):
        title = submission.title
        if target in title:
            print "\nTarget found in '%s'" % title
            log_url(my_file,submission.url)
            # email url to self

    print "\nSleeping for",secs,"seconds..."
    time.sleep(secs)

# log the urls in a text file
def log_url(file,url):
    #check if file exists
    if not os.path.isfile(my_file):
        print "\nFile %s does not exist. Creating file..." % my_file
        f = open(file,"a+")
        f.close()
    
    # open file for reading and appending
    with open(file,"r+") as f:
        if os.path.getsize(file) == 0:
            print "\n%s: File is empty. Adding '%s' to file." % (current_time(),url)
            f.write("%s\n\n" % url)
        else:
            if url in f.read():
                print "URL already in file!"
            else:
                print "\n%s: Added '%s' to file." % (current_time(),url)
                f.write("%s\n\n" % url)

def current_time():
    return time.asctime(time.localtime(time.time()))

def main():
    #TODO: get keyword and subreddit from user input
    reddit = login()
    while True:
        run_bot(reddit,"1080",'buildapcsales',50,2)

if __name__== "__main__":
    main()

