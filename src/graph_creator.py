"""
To create a hierarchical graph of the subreddits.
This will be used to cluster similar sub-reddits.
That would inherently create a hierarchy
Author: Arka Sadhu
"""
# from pathlib import Path
import networkx as nx
import pandas as pd
import wordsegment as ws


class SrGraphNode:
    """
    A Subreddit Graph Node
    Each node of NetworkX graph G will
    be an instance of this class
    """

    def __init__(self, name: str):
        self.name = name
        self.name_segments = self.word_to_subword()

    def word_to_subword(self):
        """
        Converts the given name into smaller sub-names
        Eg. 'askreddit' becomes 'ask', 'reddit'
        """
        # Note: Still noisy for cases like tifu: t, if, u
        return ws.segment(self.name)


if __name__ == '__main__':
    ws.load()
    sr_list = list(pd.read_csv('./high_filtered_srlist.csv', header=None)[0])
    G = nx.Graph()

    for sr in sr_list:
        sr_node = SrGraphNode(sr)
        G.add_node(sr_node)
