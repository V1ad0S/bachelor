import sys

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm
from termcolor import colored

from quantumoptimization.algorithms.classical_algs import goemans_williamson, greedy
from quantumoptimization.algorithms.quantum_algs import qaoa_maxcut



def get_results(G_data: np.ndarray,
                p_max: int = 1,
                use_statevec: bool = True) -> pd.DataFrame:
    col_names = ['GW', 'greedy'] + [f'qaoa(p={p})' for p in range(1, p_max + 1)]
    results = []

    try:
        for adj_list in tqdm(G_data):
            G = nx.parse_adjlist(adj_list)
            res = graph_cut_sizes(G, p_max, use_statevec)
            results.append(res)
    except:
        print(colored("Exception occured!", "red"), file=sys.stderr)

    index = pd.RangeIndex(1, len(results) + 1, name='graph_number')
    df = pd.DataFrame(results, index=index, columns=col_names)
    return df


def graph_cut_sizes(G: nx.Graph, p_max: int, use_statevec: bool) -> np.array:
    gw = goemans_williamson(G).get_cut_size()
    gr = greedy(G).get_cut_size()
    qaoa = []
    for p in range(1, p_max + 1):
        qaoa.append(qaoa_maxcut(G, p, use_statevector=use_statevec).get_cut_size())
    return np.array([gw, gr] + qaoa)