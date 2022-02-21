import os
import uuid

import pandas as pd
from termcolor import colored

from config import GRAPHRESULTS_DIR




def validate_outfilename(fname: str) -> str:
    abs_path = os.path.join(GRAPHRESULTS_DIR, fname)
    if not os.path.isfile(abs_path):
        return abs_path

    print(colored(f'File .../{fname} already exists', "yellow"))
    correct = False
    while not correct:
        new_fname = input("Enter new filename to output .csv: ")
        abs_path = os.path.join(GRAPHRESULTS_DIR, new_fname)
        if new_fname and not os.path.isfile(abs_path):
            correct = True

    return abs_path


def save_results(results_df: pd.DataFrame, out_fname: str) -> None:
    try:
        out_filename = validate_outfilename(out_fname)
    except:
        out_filename = validate_outfilename(out_fname + str(uuid.uuid4())) # random fname
        print(colored(f"\nOutput file name changed to: {out_filename}", "yellow"))

    results_df.to_csv(
        out_filename,
        index=True
    )

    print(colored(f"Results saved: {out_filename}", "green"))