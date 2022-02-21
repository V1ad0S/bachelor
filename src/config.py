import os
from pathlib import Path
from typing import NamedTuple


ROOT_DIR = os.path.dirname(Path(__file__).parent)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

GRAPH_DIR = os.path.join(DATA_DIR, 'graphs')
GRAPHINFO_DIR = os.path.join(DATA_DIR, 'graphs_info')
GRAPHRESULTS_DIR = os.path.join(DATA_DIR, 'graphs_results')


class GDataFname(NamedTuple):
    adjlist_fname: str
    info_fname: str

    def new(nodes_num: int):
        return GDataFname(
            f'graph{nodes_num}c.txt',
            f'graph{nodes_num}_info.csv'
        )