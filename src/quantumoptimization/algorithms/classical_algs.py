import networkx as nx
import numpy as np
import cvxpy as cp

from .helpers import Cut


def greedy(G: nx.Graph) -> Cut:
    left, right = set(), set()

    for vertex in G.nodes:
        l_neighbors = sum((adj in left) for adj in G.neighbors(vertex))
        r_neighbors = sum((adj in right) for adj in G.neighbors(vertex))

        if l_neighbors < r_neighbors:
            left.add(vertex)
        else:
            right.add(vertex)

    cut = Cut(G, left, right)
    return cut

def goemans_williamson(G: nx.Graph) -> Cut:
    adjacency = nx.adjacency_matrix(G).toarray()
    solution = _solve_SDP(adjacency)
    X = _factorization(solution)
    sides = _recover_cut(X)

    left = {vertex for side, vertex in zip(sides, G.nodes) if side >= 0}
    right = {vertex for side, vertex in zip(sides, G.nodes) if side < 0}
    
    return Cut(G, left, right)

def _solve_SDP(adjacency: np.ndarray) -> np.ndarray:
    Y = cp.Variable(shape=adjacency.shape, PSD=True)
    expr = cp.sum(cp.multiply(adjacency, Y))
    
    objective = cp.Minimize(expr)
    constraint = [cp.diag(Y) == 1]
    problem = cp.Problem(objective, constraint)
    problem.solve()

    return Y.value

def _factorization(Y: np.ndarray) -> np.ndarray:
    eig_vals, eig_vecs = np.linalg.eigh(Y)
    eig_vals = np.maximum(eig_vals, 0)
    eig_vals_sqrt = np.sqrt(eig_vals)
    return np.diag(eig_vals_sqrt) @ eig_vecs.T

def _recover_cut(X: np.ndarray) -> np.array:
    w = np.random.normal(size=len(X))
    projections = X.T @ w
    sides = np.sign(projections)
    return sides