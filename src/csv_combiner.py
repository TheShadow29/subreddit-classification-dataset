"""
Convenience file to merge different csv files
For the purpose of Text Classification
"""

import pandas as pd
from pathlib import Path
from tqdm import tqdm

if __name__ == '__main__':
    tdir = Path('./subr_big_csvs_hot')
    title_data = []
    for csvf in tqdm(tdir.glob('*.csv')):
        csv_data = pd.read_csv(csvf)
        # title_dict = {'label': csvf.stem, 'title': csv_data['title']}
        for ind, row in csv_data.iterrows():
            title_dict = {'label': csvf.stem, 'title': row['title']}
            title_data.append(title_dict)

    title_df = pd.DataFrame(title_data)
    title_df.to_csv('../data/all_title_data.csv', index=False)
