import networkx as nx
import numpy as np


logging_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[{asctime}] ({name}) {message}',
            'datefmt': '%H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'my_maxcut_algorithms.quantum_algs': {
            'level': 'DEBUG',
            'handlers': ['default'],
        },
        'my_maxcut_algorithms.compare': {
            'level': 'DEBUG',
            'handlers': ['default'],
        }
    }
    # 'disable_existing_loggers': True,
}


# Less luckily, qubit ordering considerations still apply. Below are some helper functions we're going to use.
# Endianness conversion tools from https://github.com/Qiskit/qiskit-terra/issues/1148#issuecomment-438574708

def state_num2str(basis_state_as_num, nqubits):
    return '{0:b}'.format(basis_state_as_num).zfill(nqubits)

def state_str2num(basis_state_as_str):
    return int(basis_state_as_str, 2)

def state_reverse(basis_state_as_num, nqubits):
    basis_state_as_str = state_num2str(basis_state_as_num, nqubits)
    new_str = basis_state_as_str[::-1]
    return state_str2num(new_str)

def get_adjusted_state(state):
    nqubits = np.log2(state.shape[0])
    if nqubits % 1:
        raise ValueError("Input vector is not a valid statevector for qubits.")
    nqubits = int(nqubits)

    adjusted_state = np.zeros(2**nqubits, dtype=complex)
    for basis_state in range(2**nqubits):
         adjusted_state[state_reverse(basis_state, nqubits)] = state[basis_state]
    return adjusted_state

# We need to get which amplitudes correspond to which basis states (bitstrings)
def state_to_ampl_counts(vec, eps=1e-15):
    """
    Converts a statevector to a dictionary
    of bitstrings and corresponding amplitudes
    """
    qubit_dims = np.log2(vec.shape[0])
    if qubit_dims % 1:
        raise ValueError("Input vector is not a valid statevector for qubits.")
    qubit_dims = int(qubit_dims)
    counts = {}
    str_format = '0{}b'.format(qubit_dims)
    for kk in range(vec.shape[0]):
        val = vec[kk]
        if abs(val) > eps:
            counts[format(kk, str_format)] = val
    return counts




# for non-integer nodes
def edges_encoder(G: nx.Graph) -> list[tuple]:
    nodes_encoder = dict(zip(G.nodes, range(G.number_of_nodes())))
    edges = []
    
    for v1, v2 in G.edges:
        i = nodes_encoder[v1]
        j = nodes_encoder[v2]
        edges.append((i, j))

    return edges


# pretty represent of graph cut with some helper functions
class Cut:
    def __init__(self, G: nx.Graph, left: set = None, right: set = None) -> None:
        self._G = G
        self._left = left if left else set()
        self._right = right if right else set()

    def __repr__(self) -> str:
        return f'left:\t{self._left}\nright:\t{self._right}'

    def add_left(self, vertex) -> None:
        self._left.add(vertex)

    def add_right(self, vertex) -> None:
        self._right.add(vertex)

    def _check_validation(self) -> None:
        # assert not nx.is_weighted(self._G)

        graph_num_nodes = self._G.number_of_nodes()
        cut_num_nodes = len(self._left) + len(self._right)
        assert graph_num_nodes == cut_num_nodes
        
        for vertex in self._G.nodes():
            assert vertex in self._left or vertex in self._right

    def get_cut_size(self) -> int:
        self._check_validation()
        return nx.cut_size(self._G, self._left, self._right)

    def draw_cutted_graph(self, ax=None) -> None:
        self._check_validation()
        node_colors = ('blue', 'red')
        edge_colors = ('brown', 'green')

        node_color_map = []
        for node in self._G.nodes:
            if node in self._right:
                node_color_map.append(node_colors[1])
            else:
                node_color_map.append(node_colors[0])

        edge_color_map = []
        edge_linewidth_map = []
        for v1, v2 in self._G.edges:
            if (v1 in self._right and v2 in self._left) or (v1 in self._left and v2 in self._right):
                edge_color_map.append(edge_colors[1])
                edge_linewidth_map.append(3)
            else:
                edge_color_map.append(edge_colors[0])
                edge_linewidth_map.append(2)

        nx.draw(self._G, with_labels=True, ax=ax,
                node_color=node_color_map,
                edge_color=edge_color_map,
                width=edge_linewidth_map)
