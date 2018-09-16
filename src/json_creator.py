"""
Creates the final json file to be submitted
Author: Arka Sadhu
"""

import json
from pathlib import Path
import pandas as pd


def get_corpus_from_csv(csvf):
    """
    Returns the corpus after reading the csv file
    """
    csv_data = pd.read_csv(csvf)
    corpus_list = []
    for _, row in csv_data.iterrows():
        tmp = {"data": str(row[0]), "label": str(row[1])}
        corpus_list.append(tmp)
    return corpus_list


if __name__ == '__main__':
    OUT_JSON = Path('../data/proposal.json')
    DESCRIPTION = ["The following dictionary contains corpus for subreddit "
                   "classification task. The corpus contains the title of the post "
                   "and the sub-reddit it was chosen from."]
    AUTHORS = {"author1": "Arka Sadhu", "author2": "Lakshmi Chirumamilla"}
    EMAILS = {"email1": "asadhu@usc.edu", "email2": "chirumam@usc.edu"}
    CSV_FILE = Path('../data/coarse_out/sample1.csv')
    CORPUS = get_corpus_from_csv(CSV_FILE)

    OUT_DICT = dict()
    OUT_DICT['description'] = DESCRIPTION
    OUT_DICT['authors'] = AUTHORS
    OUT_DICT['emails'] = EMAILS
    OUT_DICT['corpus'] = CORPUS

    json.dump(OUT_DICT, OUT_JSON.open('w'))
