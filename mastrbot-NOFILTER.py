#!/usr/bin/env python3
## assaultbot - a Mastodon bot that toots words from a dictionary with optional prefix and postfix pre/ap-pended.
## LICENSE: WTFPL
## theodric 20180310 rev1 - as assaultbot (tweepy)
## theodric 20240310 rev2 - as mastrbot (Mastodon.py)
## Thanks as always to the Python docs, StackExchange, red wine, the Oxford Comma, and my cat.

import time
import sys
from pathlib import Path
from wordfilter import Wordfilter
from mastodon import Mastodon

print("\nUsage: " + str(sys.argv[0]) + " <dictionary file>\n")

argFile = str(sys.argv[1]) # loads the contents of the file passed as an argument to the script from the CLI as variable "argfile"

##############################################################################
## CONFIGURABLE ITEMS
## Hardcode your Mastodon app key details here
## Create at https://[your-mastodon-instance]/settings/applications
## (Replace the filler, but leave the quotes.)

CLIENT_ID = 'assassassassassassassassassassassassassassass' # also called "client key" in the Mastodon Development UI
CLIENT_SECRET = 'assassassassassassassassassassassassassassass'
ACCESS_TOKEN = 'assassassassassassassassassassassassassassass'
API_BASE_URL='https://some.mastodon.service.org'
mastodon = Mastodon(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
    api_base_url=API_BASE_URL
)

## Set prefix and postfix for toots (used in for loop at bottom)
prefix = ""
postfix = ""

## Set frequency of toots posted, in SECONDS
## Don't set this too low, or you may get rate-limited.
toot_frequency = 3600 # 60 minutes, a safe value.

##############################################################################
## OK, let's roll.

## index.txt tracks our progress through the dictionary file.
## It should be stored on persistent media (so not in /tmp),
## and gets one write per iteration. N.B. for extremely write-limited disks!

## Below, we check to see if index.txt exists at the given path.
## (Edit the path, if necessary, to suit your installation!)
## If it exists, we open it and set the value of our index variable to its contents.
## If it does not exist, we create the file, then initialize it at 0.
## N.B. you can also [create and] edit this file manually in order to set a given start value.

index_check = Path("./index.txt")

if index_check.is_file():
    index_dot_txt='./index.txt'
    with open(index_dot_txt, 'r') as index_file:
        index = int(index_file.read())
else:
    print("Creating index.txt and initializing to 0...\n")
    index_dot_txt = './index.txt'
    with open(index_dot_txt, 'w') as index_file:
        index_file.write("0")
    with open(index_dot_txt, 'r') as index_file:
        index = int(index_file.read())

## Open the text file containing our dictionary.
## We are taking the argument from the command line,
## but you can also hardcode your file here by following
## the above procedure for index.txt
with open(argFile, 'r') as word_file:
    words = word_file.readlines()

## Set up Wordfilter. This is used to help us avoid auto-tooting words that are not nice.
wordfilter = Wordfilter()
## I have a few extras that I specifically do not want my bot tooting, so I add them to the filter here.
wordfilter.addWords(["rape", "rapist", "sex", "molest", "drug"])

##############################################################################
## Here we go.
## For each line in the words file, until we run out of lines, do some things:
for line in words:
    
    ## We check to see if the next word in queue is caught by Wordfilter...
    if wordfilter.blacklisted(str.upper(words[index].rstrip("\r\n"))):
        print("Yikes, " + str.upper(words[index].rstrip("\r\n")) + " might be problematic.\n We'll skip that one.")
        index += 1
    else: ## ...and if not, we continue on to toot it.
        ## Print the word at the current index, make it UPPER CASE, and chomp() the trailing newline off of it.
        ## Remove the .upper method if that's not what you want
        mastodon.status_post(prefix + str.upper(words[index].rstrip("\r\n")) + postfix)
        print("\n" + prefix + str.upper(words[index].rstrip("\r\n")) + postfix) 

        ## Increment the index value, and then write it out to disk so we keep state through restarts.
        index += 1
        with open(index_dot_txt, 'w') as index_file:
            index_file.write(str(index))
        print("\nNext toot word will be " + str.upper(words[index]))

        ## You may find this countdown annoying.
        ## If so, comment it out, and uncomment the last line instead.
        for i in range(toot_frequency, 0, -1):
            time.sleep(1)
            sys.stdout.write(str((i - 1))+' ')
            sys.stdout.flush()
        #time.sleep(toot_frequency)
