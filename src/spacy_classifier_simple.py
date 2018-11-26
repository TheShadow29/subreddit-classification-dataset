"""
Baseline approach to be used in spacy
"""
import json
from pathlib import Path
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
from spacy.util import minibatch, compounding


lab2id = json.load(open('./lab2id.json'))


def spacy_tokenizer(document):
    "Simple tokenizer"
    return [token.orth_ for token in tokenizer(document)]


def calc_print_accuracy(text_clf, test_data, test_label):
    """
    Returns accuracy for tfidf
    """
    predictions = text_clf.predict(test_data)
    clf_accuracy = np.mean(predictions == test_label) * 100.
    print(f'Test Accuracy is {clf_accuracy}')
    return clf_accuracy


def do_simple_tfidf():
    """
    Simple tfidf stuff
    """
    lab2id = json.load(open('./lab2id.json'))

    nlp = spacy.load('en')
    tokenizer = English().Defaults.create_tokenizer(nlp)
    (clean_train_data, clean_train_label), (clean_val_data,
                                            clean_val_label) = load_data(
                                                limit=200000, domap=True)

    text_lr_clf = Pipeline(
        [('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LR(verbose=1, solver='lbfgs'))])
    print('Starting to Fit')
    text_lr_clf = text_lr_clf.fit(clean_train_data, clean_train_label)
    print('Starting Evaluation')
    calc_print_accuracy(text_lr_clf, clean_val_data, clean_val_label)


def load_data(limit=18000, domap=False):

    clean_file = pd.read_csv('../data/all_title_data.csv')
    clean_file = clean_file[:limit]
    clean_data = clean_file['text']
    if domap:
        clean_label = clean_file['label'].map(lab2id)
    else:
        clean_label = clean_file['label']
    id_list = np.random.permutation(len(clean_data))
    tot_len = len(id_list)
    tr_id_list = id_list[:int(tot_len * 0.7)]
    val_id_list = id_list[int(tot_len*0.7):]
    print(
        f'Total in training set {len(tr_id_list)}, Total in validation {len(val_id_list)}')
    clean_train_data, clean_train_label = clean_data[tr_id_list], clean_label[tr_id_list]
    clean_val_data, clean_val_label = clean_data[val_id_list], clean_label[val_id_list]

    return (clean_train_data, clean_train_label), (clean_val_data, clean_val_label)


def format_data_for_spacy(texts, labs, all_labs):
    ys = []
    for true_lab in labs:
        cats = {wrong_labs: 0.0 for wrong_labs in all_labs}
        cats[true_lab] = 1.
        ys.append({'cats': cats})
    return list(zip(texts, ys))


def main(model=None, output_dir=None, n_iter=20, n_texts=18000):
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(limit=n_texts)

    train_data = format_data_for_spacy(train_texts, train_cats, lab2id)

    if 'textcat' not in nlp.pipe_names:
        textcat = nlp.create_pipe('textcat')
        nlp.add_pipe(textcat, last=True)
        # otherwise, get it, so we can add labels to it
    else:
        textcat = nlp.get_pipe('textcat')

    for l, v in lab2id.items():
        textcat.add_label(v)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']

    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print("Training the model...")
        print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
        for i in range(n_iter):
            losses = {}
            batches = minibatch(train_data, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                           losses=losses)

            with textcat.model.use_params(optimizer.averages):
                # evaluate on the dev data split off in load_data()
                scores = evaluate(nlp.tokenizer, textcat,
                                  dev_texts, dev_cats)
            print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                  .format(losses['textcat'], scores['textcat_p'],
                          scores['textcat_r'], scores['textcat_f']))

    test_text = "This movie sucked"
    doc = nlp(test_text)
    print(test_text, doc.cats)

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        print(test_text, doc2.cats)


def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}


if __name__ == '__main__':
    do_simple_tfidf()
    # main()
