"""
Main scraper file. Would include helper functions
Author: Arka Sadhu
"""
# import praw
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from reddit_crawler import get_default_reddit_inst


class Crawl:
    """
    A simple wrapper for convenient data scraping
    """

    def __init__(self, crawler=None):
        if crawler is None:
            self.crawler = get_default_reddit_inst()
        else:
            self.crawler = crawler

        self.header_lst = ['is_archived', 'num_gilded', 'is_duplicate', 'is_meta', 'is_self',
                           'perm_link', 'is_stickied', 'score', 'ups', 'downs', 'subreddit_name',
                           'title', 'text', 'create_time', 'captured_time']

    def scrape(self, subreddit, num_to_scrape=10, scrape_from='hot', out_list=None):
        """
        subreddit is either a string or
        belongs to subreddit class from praw
        num_to_scrape: number of submissions to scrape
        scrape_from which mode to scrape from
        out_list to be returned
        """
        # If string convert to subreddit type which
        # be used for querying
        if isinstance(subreddit, str):
            subreddit = self.crawler.subreddit(subreddit)

        # Get the following fields:
        # archived, gilded, duplicates exist,
        # is_meta, is_self, permalink,
        # stickied, score, ups, downs,
        # subreddit name, title, selftext
        # created_at_utc, captured_at_utc
        # Need the scrape_from to belong to one of the
        # given categories
        assert hasattr(subreddit, scrape_from)
        subm_generator = getattr(subreddit, scrape_from)
        if out_list is None:
            out_list = []
        for subm in tqdm(subm_generator(limit=num_to_scrape), total=num_to_scrape):
            is_archived = subm.archived
            num_gilded = subm.gilded
            is_duplicate = len(list(subm.duplicates())) > 0
            is_meta = subm.is_meta
            is_self = subm.is_self
            perm_link = subm.permalink
            is_stickied = subm.stickied
            score = subm.score
            ups = subm.ups
            downs = subm.downs
            subreddit_name = subm.subreddit.display_name
            title = subm.title
            text = subm.selftext
            create_time = str(datetime.utcfromtimestamp(subm.created_utc))
            captured_time = str(datetime.utcnow())
            tmp_lst = [is_archived, num_gilded, is_duplicate, is_meta, is_self, perm_link,
                       is_stickied, score, ups, downs, subreddit_name, title, text, create_time,
                       captured_time]
            out_list.append(tmp_lst)

        return out_list


if __name__ == '__main__':
    small_sr_list = list(pd.read_csv(
        './high_filtered_srlist.csv', header=None)[0])
    cr = Crawl()
    for i, sr in enumerate(small_sr_list[:1]):
        olist = cr.scrape('askreddit', num_to_scrape=5000)
        df_out = pd.DataFrame(olist, columns=cr.header_lst)
        df_out.to_csv(f'./subr_csvs/{sr}.csv', index=False, header=True)
        print(i, f'Finished {sr} subreddit')
