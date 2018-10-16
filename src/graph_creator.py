"""
To create a hierarchical graph of the subreddits.
This will be used to cluster similar sub-reddits.
That would inherently create a hierarchy
Author: Arka Sadhu
"""
# from pathlib import Path
import itertools
import json
import pickle
import numpy as np
import pandas as pd
import networkx as nx
import wordsegment as ws
import spacy
from sklearn import metrics
from tqdm import tqdm


class SrGraphNode:
    """
    A Subreddit Graph Node
    Each node of NetworkX graph G will
    be an instance of this class
    """

    def __init__(self, name: str):
        self.name = name.lower()
        self.name_segments = self.word_to_subword()
        self.we_lst = None
        self.pub_desc = None

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

    @classmethod
    def init_from_iloc(cls, iloc):
        """
        Initialize using row of the csv
        """
        name = iloc['subreddit_name']
        return cls(name)

    def set_pub_desc(self, iloc):
        """
        Set the public_description separately
        """
        self.pub_desc = iloc['public_description']

    def __str__(self):
        """
        Return the name when printing the node
        """
        return self.name


def full_sim(sr_node1, sr_node2):
    """
    Computes similarity between two nodes of the graph
    """
    cos_sim = metrics.pairwise.cosine_similarity(
        sr_node1.we_lst.tensor, sr_node2.we_lst.tensor)
    return np.mean([cos_sim.mean(), cos_sim.max()])


class Grapher:
    """
    A wrapper around networkx graph to store relevant things
    """

    def __init__(self):
        self.G = nx.Graph()
        self.id_to_node_dict = None
        self.name_to_node_dict = None

    def create_graph_nodes_from_ilocs(self, sub_df, nlp_spacy):
        """
        Creates the nodes of the graph reading the df
        """
        # Create the Nodes for the graph
        for _, sr_row in sub_df.iterrows():
            sr_node = SrGraphNode.init_from_iloc(sr_row)
            # sr_node.set_pub_desc(sr_row)
            sr_node.get_embedding_list(nlp_spacy)
            self.G.add_node(sr_node)

    def create_id_mapping(self):
        """
        Creates id to node mapping for easy access
        """
        # Create a mapping for easy access
        self.id_to_node_dict = {i: n for i, n in enumerate(self.G.nodes)}
        self.name_to_node_dict = {str(n): n for n in self.G.nodes}

    def create_fc_graph(self, _cfg):
        """
        Create fully connected graph
        """
        # Create Fully connected graph
        comb = itertools.combinations(np.arange(len(self.id_to_node_dict)), 2)
        sim_thresh = _cfg['sim_thresh']
        tot_nodes = len(self.id_to_node_dict)
        tot_comb = tot_nodes * (tot_nodes - 1) // 2
        for c in tqdm(comb, total=tot_comb):
            n1 = self.id_to_node_dict[c[0]]
            n2 = self.id_to_node_dict[c[1]]
            sim = full_sim(n1, n2)
            if sim > sim_thresh:
                self.G.add_edge(n1, n2, sim=sim,
                                weight1=1-sim, weight2=1/sim)


def get_default_graph():
    """
    Convenience function to get default graph
    """
    cfg = json.load(open('./config.json'))
    ws.load()
    nlp = spacy.load('en_core_web_md')
    sr_df = pd.read_csv('./low_filtered_strict.csv')
    grapher = Grapher()
    grapher.create_graph_nodes_from_ilocs(sr_df, nlp)
    grapher.create_id_mapping()
    grapher.create_fc_graph(cfg)
    return grapher


def read_saved_graph(fname):
    """
    Convenience function to read graph from file
    """
    return pickle.load(open(fname, 'rb'))


if __name__ == '__main__':
    pass
    # cfg = json.load(open('./config.json'))
    # ws.load()
    # nlp = spacy.load('en_core_web_md')
    # # sr_list = list(pd.read_csv('./high_filtered_srlist.csv', header=None)[0])
    # # sr_list = list(pd.read_csv('./low_filtered_strict.csv')
    # #                ['subreddit_name'])
    # sr_df = pd.read_csv('./low_filtered_strict.csv')
    # grapher = Grapher()
    # grapher.create_graph_nodes_from_ilocs(sr_df)
    # grapher.create_id_mapping()
    # grapher.create_fc_graph(cfg)
