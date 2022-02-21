from scripts.solve import get_results
from scripts.load_graphdata import load_graphs, GDataFname
from scripts.save_graphdata import save_results


def solve_dataset(
            graphdata_fname: str,
            p_max: int = 1,
            part_range: tuple[int] = None
        ) -> None:
    G_data = load_graphs(graphdata_fname)
    res_df = get_results(G_data, p_max, part_range=part_range)
    out_fname = graphdata_fname.replace('.txt', '.csv')
    if part_range:
        out_fname = f"part_({res_df.index[0]}-{res_df.index[-1]})" + out_fname
    save_results(res_df, out_fname)


if __name__ == "__main__":
    fname = GDataFname.new(8)
    solve_dataset(fname.adjlist_fname, p_max=3, part_range=(514, 11117))