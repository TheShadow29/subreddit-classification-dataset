"""
Utility file to preprocess and clean up the csv data
"""
from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    csvf = pd.read_csv('../data/all_title_data.csv')
    csvf.title = csvf.title.str.replace(r'\[.*\]', '')
    csvf.title = csvf.title.str.replace(r'\(.*\)', '')
    csvf.to_csv('../data/all_title_cleaned_data.csv', index=False)
    
