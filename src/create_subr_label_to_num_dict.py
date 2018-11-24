"""
Util to create a small dictionary mapping subreddit name to id
"""

import pandas as pd
import json

if __name__ == '__main__':
    subr_list = pd.read_csv('./low_filtered_strict.csv')['subreddit_name']
    subr_dict = dict(subr_list)
    inv_dict = {v: k for k, v in subr_dict.items()}

    json.dump(subr_dict, open('id2lab.json', 'w'))
    json.dump(inv_dict, open('lab2id.json', 'w'))
