import praw
import config
import time
import os
import sys

my_file = "log.txt"
count = 0
secs = 2

# log into reddit using config.py
def login():
    print "Logging in..."
    
    reddit = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "GPU Alert Bot")
    
    print "Logged in as %s" % config.username
            
    return reddit

# searches for a target word in a specific subreddit and prints out the count
def run_bot(reddit,target,sub,lim):
    subreddit = reddit.subreddit(sub)
    
    for submission in subreddit.new(limit = lim):
        title = submission.title
        if target.lower() in title.lower():
            print "\nTarget found in '%s'" % title
            log_url(my_file,submission.url)
            # email url to self

    sleep()

# log the urls in a text file
def log_url(file,url):
    global count
    
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
                count = count + 1
            else:
                print "\n%s: Added '%s' to file." % (current_time(),url)
                f.write("%s\n\n" % url)

def current_time():
    return time.asctime(time.localtime(time.time()))

def sleep():
    global count,secs
    
    # TODO: change 50 to constant threshold
    if count > 50:
        print "\nThreshold hit."
        count = 0
        secs = 60
    else:
        secs = 2

    print "\nSleeping for %d seconds... count is %d" % (secs,count)
    time.sleep(secs)

def user_input():
    try:
        keyword = raw_input("\nEnter a keyword to search: ")
        return keyword
    except (EOFError,KeyboardInterrupt):
        print "\nExiting %s" % sys.argv[0]
        sys.exit(0)

def main():
    reddit = login()

    keyword = user_input()

    while True:
        print "\nPress CTRL-C to exit program at any time."
        try:
            run_bot(reddit,keyword,'buildapcsales',50)
        except (EOFError,KeyboardInterrupt):
            print "\nExiting %s" % sys.argv[0]
            sys.exit(0)

if __name__== "__main__":
    main()

