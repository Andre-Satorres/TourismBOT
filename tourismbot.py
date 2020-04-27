import tweepy
import time
import random

print('this is my twitter bot')

CONSUMER_KEY = '****'
CONSUMER_SECRET = '********'
ACCESS_KEY = '*********'
ACCESS_SECRET = '***********'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(filename):
    file_read = open(filename, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, filename):
    file_write = open(filename, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


def select_place():
    id = random.randint(1, 25)
    return id


def get_image_info(filename, id):
    file_read = open(filename, 'r')
    lines = file_read.readlines()
    return lines[id-1]


def reply_to_tweets():
    print('retrieving and replying tweets...')

    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if 'place' in mention.full_text.lower():
            print("Found 'place'!")
            print('Responding back...')

            image_id = select_place()
            image_path = 'places/' + str(image_id) + '.jpg'
            image_info = get_image_info("images", image_id)

            status = '@' + mention.user.screen_name + ' A great place to travel to you: ' + image_info

            api.update_with_media(image_path, status, in_reply_to_status_id=mention.id)


while 1:
    reply_to_tweets()
    time.sleep(25)
