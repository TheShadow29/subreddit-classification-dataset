"""
Convenience file to read the all subreddit file
Author: Arka Sadhu
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from reddit_crawler import get_default_reddit_inst
# import praw
# from tqdm import tqdm


class SubrFilter:
    """
    A generic object class to filter the subreddit list
    """

    def __init__(self, _sub_red_info, _red_crawler, _cfg):
        self.sub_red_info = _sub_red_info
        self.red_crawler = _red_crawler
        self.cfg = _cfg

    def filter_min_sub_count(self):
        """
        Removes subreddits with less than min count
        """
        # Set minimum count
        min_sub_count = self.cfg['min_sub_count']
        # filter out subreddits based on min subscribers_count
        self.sub_red_info = self.sub_red_info[self.sub_red_info.subscribers_count > min_sub_count]

    def create_subr_instances(self):
        """
        Creates subreddit instances
        """
        # Make corresponding instances
        tmp = self.sub_red_info.subreddit_name.apply(
            lambda x: self.red_crawler.subreddit(x))
        self.sub_red_info = self.sub_red_info.assign(subreddit=np.array(tmp))

    def filter_non_text_strict(self):
        """
        Simply looks at the subreddit properties
        if image/video/gifs allowed then they are removed
        Note: Use keep_only_text_strict from now on
        """
        print(len(self.sub_red_info))
        tmp_bool_df = self.sub_red_info.subreddit.apply(
            lambda x: not x.allow_images)
        self.sub_red_info = self.sub_red_info[tmp_bool_df]

    def keep_only_text_strict(self):
        """
        Assumes the csv already has all relevant columns
        """
        tmp_bool_df = self.sub_red_info.apply(lambda row: not(
            row.allw_imgs or row.allw_vids or row.allw_gifs or row.over18), axis=1)
        self.sub_red_info = self.sub_red_info[tmp_bool_df]


def get_default_filtered_list():
    """
    Convenience function to get default filtered list
    """
    # csv_file = Path('/scratch/arka/Ark_git_files/subr/subreddits_public.csv')
    csv_file = Path('./req_subr_without_pub_desc.csv')
    sub_red_info = pd.read_csv(csv_file)
    # Convert the subscribers_count into ints and remove None/NaN by setting them to 0
    sub_red_info.subscribers_count = pd.to_numeric(
        sub_red_info.subscribers_count, errors='coerce').fillna(0).astype(np.int_)
    # load config file
    cfg = json.load(open('./config.json', 'r'))

    # Init Reddit crawler
    red_crawler = get_default_reddit_inst()

    sub_filter = SubrFilter(sub_red_info, red_crawler, cfg)
    sub_filter.filter_min_sub_count()
    # sub_filter.create_subr_instances()
    # sub_filter.filter_non_text_strict()
    sub_filter.keep_only_text_strict()
    return sub_filter.sub_red_info


if __name__ == '__main__':
    subr_filter = get_default_filtered_list()
    # subr_filter.subreddit_name.to_csv(
    # 'high_filtered_srlist.csv', index=False, header=False)
