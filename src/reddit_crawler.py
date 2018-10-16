"""
Author: Arka Sadhu
This is the main file to crawl reddit and save the extracted information.
"""
import json
from pathlib import Path
import praw
import pandas as pd
from tqdm import tqdm


def get_posts_for_reddit_list(rinst, rlist, lim=10):
    """
    First is the reddit instance via praw
    Expects a list of strings
    Each string is a subreddit
    Limit is number of submissions to look at
    Output is a dataframe with two columns
    Title of the Post, Subreddit it was taken from
    """
    out_list = []
    for subr in tqdm(rlist):
        for subm in rinst.subreddit(subr).hot(limit=lim):
            tmp = [subm.title, subr]
            out_list.append(tmp)

    return pd.DataFrame(out_list, columns=['Title', 'Subreddit'])


def get_default_reddit_inst():
    """
    Helper function to get default reddit instance
    """
    return praw.Reddit('scraper')


if __name__ == '__main__':
    # Defining paths
    SRC_JSON = Path('./small_list_subreddit.json')
    CSLIST = 'coarse_slist'
    FGLIST = 'fine_slist'
    SRC_MAIN = json.load(SRC_JSON.open('r'))
    OUT_DIR = Path('../data/')
    COARSE_OUT_DIR = OUT_DIR / 'coarse_out'
    FG_OUT_DIR = OUT_DIR / 'fine_grained_out'
    COARSE_OUT_DIR.mkdir(exist_ok=True)
    FG_OUT_DIR.mkdir(exist_ok=True)

    # Defining Reddit Instance to be used for scrapping
    REDDIT_INST = praw.Reddit('scraper')

    CO_SLIST = SRC_MAIN[CSLIST]
    FG_SLIST = SRC_MAIN[FGLIST]

    assert isinstance(CO_SLIST, list)
    assert isinstance(FG_SLIST, list)

    CO_DF = get_posts_for_reddit_list(REDDIT_INST, CO_SLIST)
    FG_DF = get_posts_for_reddit_list(REDDIT_INST, FG_SLIST)

    CO_DF.to_csv(COARSE_OUT_DIR / 'sample1.csv', index=False)
    FG_DF.to_csv(FG_OUT_DIR / 'sample1.csv', index=False)
