import os

import numpy as np
import pandas as pd

from config import GRAPH_DIR, GRAPHINFO_DIR, GRAPHRESULTS_DIR, GDataFname



def load_graphs(filename: str) -> np.ndarray:
    def parse_adjlist(adj_list: str) -> list[str]:
        return adj_list.split(';')

    data = np.loadtxt(
        fname=os.path.join(GRAPH_DIR, filename),
        encoding='utf-8',
        delimiter=':',
        usecols=1,
        converters={1: parse_adjlist},
        dtype=str,
    )

    return data


def load_graphs_info(filename: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(GRAPHINFO_DIR, filename), index_col=0)


def load_graphs_results(filename: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(GRAPHRESULTS_DIR, filename), index_col=0)


def load_graphs_dataset(nodes_num: int, info: bool = False):
    fname = GDataFname.new(nodes_num)
    G_data = load_graphs(fname.adjlist_fname)
    G_res  = load_graphs_results(fname.adjlist_fname)
    if info:
        G_info = load_graphs_info(fname.info_fname)
        return G_data, G_res, G_info
    return G_data, G_res