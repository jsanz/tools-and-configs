#!/usr/bin/env python3
"""
Script to remove tweets older than a given number of days
"""

import time
from datetime import date
import twitter
from dateutil.parser import parse
import sqlite3
import logging
import os


logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s [%(levelname)-7s] %(message)s',
    datefmt='%y-%m-%d | %I:%M:%S %p')
logger = logging.getLogger('beekeeper')

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_tweets(api=None, screen_name=None):
    """
    Helper function to get the timeline of a given user
    """
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    logger.info("getting tweets before: {}".format(str(earliest_tweet)))

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            logger.info("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


if __name__ == "__main__":
    DAYS = 10
    BACKUP_DB = os.getenv("TW_BACKUP")

    logger.info("Removing tweets older than {} days".format(DAYS))

    # creating the twitter api obj
    api = twitter.Api(
        consumer_key=os.getenv("TW_C_KEY"),
        consumer_secret=os.getenv("TW_C_SECRET"),
        access_token_key=os.getenv("TW_T_KEY"),
        access_token_secret=os.getenv("TW_T_SECRET"),
    )

    conn = sqlite3.connect(BACKUP_DB)
    cursor = conn.cursor()

    # asking for my tweets and removing those older than a month
    screen_name = os.getenv("TW_USER")
    timeline = get_tweets(api=api, screen_name=screen_name)

    def filter_func(row):
        dif = date.today() - parse(row.created_at, ignoretz=True).date()
        return dif.days > DAYS

    old_timeline = list(filter(filter_func, timeline))
    logger.info("{} tweets to remove".format(len(old_timeline)))

    for t in old_timeline:
        logger.info("Removing {}...".format(t.id))
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO tweets (id, json) VALUES ( ?, ? )",
                (t.id, t.AsJsonString()),
            )
            conn.commit()
            api.DestroyStatus(t.id)
        except Exception as e:
            logger.error(e)
        time.sleep(0.5)
    conn.close()
    logger.info("Done!")
