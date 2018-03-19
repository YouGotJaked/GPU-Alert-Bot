import praw
import config
import time
import os.path

my_file = "gpu.txt"

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
            log_url(my_file,submission.url)
            # email url to self

    print "Sleeping for",secs,"seconds..."
    time.sleep(secs)

# log the urls in a text file
def log_url(file,url):
    # open file for reading and appending
    with open(file,"a+") as f:
            print "\nAdded %s to file on %s" % (url,current_time())
            f.write("%s\n\n" % url)

def current_time():
    return time.asctime(time.localtime(time.time()))

def main():
    reddit = login()
    while True:
        run_bot(reddit,"1080",'buildapcsales',25,2)

if __name__== "__main__":
    main()

