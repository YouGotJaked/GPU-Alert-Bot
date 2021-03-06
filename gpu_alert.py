import praw
import config
import time
import os
import sys
import smtplib
from email.mime.text import MIMEText

email_file = "gmail.txt"
log_file = "log.txt"
count = 0
secs = 2

class Email():
    def __init__(self, addr, password):
        self.addr = addr
        self.password = password

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
            if log_url(log_file,submission.url):
                send_email(title,submission.url)
    sleep()

# log the urls in a text file
def log_url(file,url):
    global count
    
    #check if file exists
    if not os.path.isfile(log_file):
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
                return False
            else:
                print "\n%s: Added '%s' to file." % (current_time(),url)
                f.write("%s\n\n" % url)
        return True

def send_email(title,url):
    my_email = get_email(email_file)
    addr = my_email.addr
    password = my_email.password
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(addr, password)
    except:
        print "Could not connect to email server."

    msg = MIMEText(url)
    msg['Subject'] = title
    msg['From'] = addr
    msg['To'] = addr
    server.sendmail(addr, [addr], msg.as_string())
    server.quit()

def get_email(file):
    with open(file) as f:
        lines = f.readlines()
    #remove whitespace characters
    lines = [x.strip() for x in lines]
    return Email(lines[0], lines[1])

def current_time():
    return time.asctime(time.localtime(time.time()))

def sleep():
    global count,secs
    
    # TODO: change 25 to constant threshold
    if count > 25:
        print "\nThreshold hit."
        count = 0
        secs = 60
    elif secs != 2:
        secs = 2

    print "\nSleeping for %d seconds..." % secs
    time.sleep(secs)

def user_input():
    try:
        keyword = raw_input("\nEnter a keyword to search: ")
        subreddit = raw_input("\nEnter a subreddit to search: ")
        return keyword,subreddit
    except (EOFError,KeyboardInterrupt):
        print "\nExiting %s" % sys.argv[0]
        sys.exit(0)

def main():
    reddit = login()
    keyword,subreddit = user_input()

    while True:
        print "\nPress CTRL-C to exit program at any time."
        try:
            run_bot(reddit,keyword,subreddit,150)
        except (EOFError,KeyboardInterrupt):
            print "\nExiting %s" % sys.argv[0]
            sys.exit(0)

if __name__== "__main__":
    main()

