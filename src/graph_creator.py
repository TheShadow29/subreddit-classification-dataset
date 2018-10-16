"""
To create a hierarchical graph of the subreddits.
This will be used to cluster similar sub-reddits.
That would inherently create a hierarchy
Author: Arka Sadhu
"""
# from pathlib import Path
import itertools
import json
import numpy as np
import pandas as pd
import networkx as nx
import wordsegment as ws
import spacy
from sklearn import metrics


class SrGraphNode:
    """
    A Subreddit Graph Node
    Each node of NetworkX graph G will
    be an instance of this class
    """

    def __init__(self, name: str):
        self.name = name
        self.name_segments = self.word_to_subword()
        self.we_lst = None

    def word_to_subword(self):
        """
        Converts the given name into smaller sub-names
        Eg. 'askreddit' becomes 'ask', 'reddit'
        """
        # Note: Still noisy for cases like tifu: t, if, u
        return ws.segment(self.name)

    def get_embedding_list(self, embedder):
        """
        Wrapper aroud the spacy embedder
        """
        self.we_lst = embedder(' '.join(self.name_segments))


def full_sim(sr_node1, sr_node2):
    """
    Computes similarity between two nodes of the graph
    """
    cos_sim = metrics.pairwise.cosine_similarity(
        sr_node1.we_lst.tensor, sr_node2.we_lst.tensor)
    return np.mean([cos_sim.mean(), cos_sim.max()])


if __name__ == '__main__':
    cfg = json.load(open('./config.json'))
    ws.load()
    nlp = spacy.load('en_core_web_md')
    sr_list = list(pd.read_csv('./high_filtered_srlist.csv', header=None)[0])
    G = nx.Graph()

    # Create the Nodes for the graph
    for sr in sr_list:
        sr_node = SrGraphNode(sr)
        sr_node.get_embedding_list(nlp)
        G.add_node(sr_node)

    # Create a mapping for easy access
    id_to_node_dict = {i: n for i, n in enumerate(G.nodes)}
    # Create Fully connected graph
    comb = itertools.combinations(np.arange(len(id_to_node_dict)), 2)
    sim_thresh = cfg['sim_thresh']
    for c in comb:
        n1 = id_to_node_dict[c[0]]
        n2 = id_to_node_dict[c[1]]
        sim = full_sim(n1, n2)
        if sim > sim_thresh:
            G.add_edge(n1, n2, sim=sim)
