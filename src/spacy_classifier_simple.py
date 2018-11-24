"""
Baseline approach to be used in spacy
"""
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression as LR
from sklearn.pipeline import Pipeline

import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en')
tokenizer = English().Defaults.create_tokenizer(nlp)


def spacy_tokenizer(document):
    return [token.orth_ for token in tokenizer(document)]


def calc_print_accuracy(text_clf, test_data, test_label):
    predictions = text_clf.predict(test_data)
    clf_accuracy = np.mean(predictions == test_label) * 100.
    print(f'Test Accuracy is {clf_accuracy}')
    return clf_accuracy


if __name__ == '__main__':
    lab2id = json.load(open('./lab2id.json'))

    clean_file = pd.read_csv('../data/all_title_data.csv')
    clean_file = clean_file[:200000]
    clean_data = clean_file['title']
    clean_label = clean_file['label'].map(lab2id)

    id_list = np.random.permutation(len(clean_data))
    tot_len = len(id_list)
    tr_id_list = id_list[:int(tot_len * 0.7)]
    val_id_list = id_list[int(tot_len*0.7):]
    print(
        f'Total in training set {len(tr_id_list)}, Total in validation {len(val_id_list)}')
    clean_train_data, clean_train_label = clean_data[tr_id_list], clean_label[tr_id_list]
    clean_val_data, clean_val_label = clean_data[val_id_list], clean_label[val_id_list]

    text_lr_clf = Pipeline(
        [('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LR(verbose=1, solver='lbfgs'))])
    print('Starting to Fit')
    text_lr_clf = text_lr_clf.fit(clean_train_data, clean_train_label)
    print('Starting Evaluation')
    calc_print_accuracy(text_lr_clf, clean_val_data, clean_val_label)
