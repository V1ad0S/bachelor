import sys

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm
from termcolor import colored

from quantumoptimization.algorithms.classical_algs import goemans_williamson, greedy
from quantumoptimization.algorithms.quantum_algs import qaoa_maxcut



def get_results(
            G_data: np.ndarray,
            p_max: int = 1,
            use_statevec: bool = True,
            part_range: tuple[int] = None,
        ) -> pd.DataFrame:
    col_names = ['GW', 'greedy'] + [f'qaoa(p={p})' for p in range(1, p_max + 1)]
    results = []

    if not part_range:
        part_range = (0, len(G_data) + 1)

    data = G_data[part_range[0] - 1 : part_range[1]]

    try:
        for adj_list in tqdm(data):
            G = nx.parse_adjlist(adj_list)
            res = graph_cut_sizes(G, p_max, use_statevec)
            results.append(res)
    except:
        print(colored("Exception occured!", "red"), file=sys.stderr)

    index = pd.RangeIndex(
        part_range[0],
        part_range[0] + len(results),
        name='graph_number'
    )

    try:
        df = pd.DataFrame(results, index=index, columns=col_names)
    except:
        df = pd.DataFrame(results, columns=col_names)

    return df


def graph_cut_sizes(G: nx.Graph, p_max: int, use_statevec: bool) -> np.array:
    gw = goemans_williamson(G).get_cut_size()
    gr = greedy(G).get_cut_size()
    qaoa = []
    for p in range(1, p_max + 1):
        qaoa.append(qaoa_maxcut(G, p, use_statevector=use_statevec).get_cut_size())
    return np.array([gw, gr] + qaoa)