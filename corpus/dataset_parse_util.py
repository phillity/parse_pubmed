import os
import spacy
import numpy as np
from networkx import Graph, DiGraph, descendants, shortest_path


np.random.seed(42)


# part of speech dict
# https://universaldependencies.org/u/pos/
POS = {'adj': 0, 'adp': 1, 'adv': 2, 'aux': 3, 'cconj': 4, 'conj': 5, 'det': 6, 'intj': 7, 'noun': 8,
       'num': 9, 'part': 10, 'pron': 11, 'propn': 12, 'punct': 13, 'sconj': 14, 'sym': 15, 'verb': 16, 'x': 17}
# dependency dict
# https://universaldependencies.org/u/dep/
DEP = {'acl': 0, 'acomp': 1, 'advcl': 2, 'advmod': 3, 'agent': 4, 'amod': 5, 'appos': 6, 'attr': 7, 'aux': 8, 'auxpass': 9, 'case': 10, 'cc': 11, 'ccomp': 12, 'complm': 13, 'compound': 14, 'conj': 15, 'csubj': 16, 'csubjpass': 17, 'dative': 18, 'dep': 19, 'det': 20, 'dobj': 21, 'expl': 22, 'hmod': 23, 'hyph': 24, 'infmod': 25, 'intj': 26, 'iobj': 27, 'mark': 28, 'meta': 29,
       'neg': 30, 'nmod': 31, 'nn': 32, 'nounmod': 33, 'npadvmod': 34, 'npmod': 35, 'nsubj': 36, 'nsubjpass': 37, 'num': 38, 'number': 39, 'nummod': 40, 'oprd': 41, 'parataxis': 42, 'partmod': 43, 'pcomp': 44, 'pobj': 45, 'poss': 46, 'possessive': 47, 'preconj': 48, 'predet': 49, 'prep': 50, 'prt': 51, 'punct': 52, 'quantmod': 53, 'rcmod': 54, 'relcl': 55, 'root': 56, 'xcomp': 57}


def parse_sp(x, y, doc, nlp):
    # Get undirected graph
    graph_edges = []
    for token in doc:
        if x in token.lower_:
            x = token.lower_
        if y in token.lower_:
            y = token.lower_
        for child in token.children:
            graph_edges.append((token.lower_ + str(token.i),
                                child.lower_ + str(child.i)))
    undirected_graph = Graph(graph_edges)

    # Shortest path between x and y
    p = []
    sp = shortest_path(undirected_graph, source=x, target=y)
    for token in doc:
        for child in token.children:
            if token.lower_ + str(token.i) in sp and child.lower_ + str(child.i) in sp:
                if token.lower_ == x.lower_ and child.lower_ == y.lower_:
                    p.append(("x",
                              token.pos_.lower(),
                              child.dep_,
                              "y"))
                elif token.lower_ == y.lower_ and child.lower_ == x.lower_:
                    p.append(("y",
                              token.pos_.lower(),
                              child.dep_,
                              "x"))
                elif token.lower_ == x.lower_:
                    p.append(("x",
                              token.pos_.lower(),
                              child.dep_,
                              child.lemma_.lower()))
                elif child.lower_ == x.lower_:
                    p.append((token.lemma_.lower(),
                              token.pos_.lower(),
                              child.dep_,
                              "x"))
                elif token.lower_ == y.lower_:
                    p.append(("y",
                              token.pos_.lower(),
                              child.dep_,
                              child.lemma_.lower()))
                elif child.lower_ == y.lower_:
                    p.append((token.lemma_.lower(),
                              token.pos_.lower(),
                              child.dep_,
                              "y"))
                else:
                    p.append((token.lemma_.lower(),
                              token.pos_.lower(),
                              child.dep_,
                              child.lemma_.lower()))
    return np.array(p).tolist()