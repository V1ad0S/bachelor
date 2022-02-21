import logging
import logging.config

import matplotlib.pyplot as plt
import networkx as nx

from .quantum_algs import qaoa_maxcut
from .classical_algs import greedy, goemans_williamson
from .helpers import logging_config


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


class Comparer:
    def __init__(self, G: nx.Graph) -> None:
        self.G = G

        self.GW = goemans_williamson
        self.greedy = greedy
        self.QAOA = qaoa_maxcut

        self.cut = None

    def solve(self, G: nx.Graph = None, **qaoa_kwargs):
        if not G:
            G = self.G

        cut_GW = self.GW(G)
        logger.info('GW: done')
        cut_greedy = self.greedy(G)
        logger.info('greedy: done')
        cut_qaoa = self.QAOA(G, **qaoa_kwargs)
        
        if cut_qaoa:
            logger.info('QAOA: done')
        else:
            logger.warning('QAOA: ERROR!')

        self.cut = {
            'GW': cut_GW,
            'greedy': cut_greedy,
            'QAOA': cut_qaoa,
        }
    
    def make_plot(self) -> plt.Figure:
        if not self.cut:
            print('At first run `.solve`-method')
            return
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        nx.draw(self.G, with_labels=True, ax=axes[0][0])
        axes[0][0].set_title('Original')

        for ax, (key, cut) in zip(axes.flatten()[1:], self.cut.items()):
            if not cut:
                continue
            cut.draw_cutted_graph(ax=ax)
            ax.set_title(key)
        return fig
    
    def __repr__(self) -> str:
        if not self.cut:
            return "Not solved!"
        res = ""
        for alg, cut in self.cut.items():
            if not cut:
                res += f"{alg}: not solved!"
                continue
            res += f"{alg}:\t{cut.get_cut_size()}\n"
        return res