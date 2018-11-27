"""
Convenience file to merge different csv files
For the purpose of Text Classification
"""

import pandas as pd
from pathlib import Path
from tqdm import tqdm
from collections import Counter


def combine_csv_by_sr_type(sr_type='hot'):
    tdir = Path(f'./subr_big_csvs_{sr_type}')
    title_data = []
    considered_csvs = set(list(pd.read_csv(
        './considered_csvs_after_clean.csv', header=None)[0]))
    for csvf in tqdm(tdir.glob('*.csv')):
        if csvf.stem not in considered_csvs:
            continue
        csv_data = pd.read_csv(csvf)
        csv_data = csv_data.dropna(subset=['title'])
        # if len(csv_data) < 100:
        # continue
        # considered_csvs.append(csvf.stem)

        csv_data.title = csv_data.title.str.replace(r'\[.*\]', '')
        csv_data.title = csv_data.title.str.replace(r'\(.*\)', '')
        csv_data.title = csv_data.title.str.replace(r'\{.*\}', '')
        all_titles = Counter(' '.join(list(csv_data['title'])).split(' '))
        most_common = all_titles.most_common(1)[0]
        most_common_word, most_common_freq = most_common
        if most_common_freq > 0.9 * len(csv_data):
            csv_data['title'] = csv_data['title'].str.replace(
                most_common_word, '')

        for ind, row in csv_data.iterrows():
            if len(row['title'].split(' ')) < 5:
                continue
            title_dict = {'label': csvf.stem, 'title': row['title']}
            title_data.append(title_dict)

    title_df = pd.DataFrame(title_data)
    title_df = title_df.rename(index=str, columns={'title': 'text'})

    title_df.to_csv(
        f'../data/cleaned_all_title_data_{sr_type}.csv', index=False)
    # cons_csvs = pd.DataFrame(considered_csvs)
    # cons_csvs.to_csv('./considered_csvs_after_clean.csv',
    #                  index=False, header=False)


if __name__ == '__main__':
    cleaned_data_hot = pd.read_csv('../data/cleaned_all_title_data_hot.csv')
    cleaned_data_top = pd.read_csv('../data/cleaned_all_title_data_top.csv')
    cleaned_data_cont = pd.read_csv(
        '../data/cleaned_all_title_data_controversial.csv')
