from scripts.solve import get_results
from scripts.load_graphdata import load_graphs, GDataFname
from scripts.save_graphdata import save_results


def solve_whole_dataset(graphdata_fname: str, p_max: int = 1) -> None:
    G_data = load_graphs(graphdata_fname)
    res_df = get_results(G_data, p_max)
    save_results(res_df, graphdata_fname.replace('.txt', '.csv'))


if __name__ == "__main__":
    fname = GDataFname.new(8)
    solve_whole_dataset(fname.adjlist_fname, p_max=3)