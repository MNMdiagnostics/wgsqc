import sys
sys.path.append("..")
import pandas as pd
import os
import time
import statistics
from new_database.new_base import engine


def add_to_database_from_files(root_directory, engine):
    """
    Adds records to database from nested directory of a tab separated files.

    :param root_directory: Path to directory containing subdirectories with files.
    :param base:
    """
    colnames = ("transcript_id", "gene_id", "mean_coverage", "percentage_above_10", "percentage_above_20", "percentage_above_30")
    total = time.perf_counter()
    times = []
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            print("CURRENT FILE:", file)
            t = time.perf_counter()
            file_absolute_path = os.path.join(subdir, file)
            table = pd.read_csv(file_absolute_path, sep="\t", header=None, names=colnames)
            table['sample_id'] = os.path.basename(subdir)
            table.to_sql('wgs_qc', engine, if_exists='append', index=False)
            print(f"FILE {file} ADDED TO DATABASE, EXECUTION TIME: {round(time.perf_counter() - t, 2)}")
            times.append(time.perf_counter() - t)
    print(f"\n\nTOTAL TIME: {time.perf_counter() - total}")
    print(f"MAX TIME: {round(max(times), 2)}")
    print(f"MIN TIME: {round(min(times), 2)}")
    print(f"MEAN TIME: {round(statistics.mean(times), 2)}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        rootdir = sys.argv[1]

    elif len(sys.argv) == 2:
        rootdir = sys.argv[1]

    elif len(sys.argv) == 1:
        print("Root directory set up as /home/username")
        rootdir = "~/"

    add_to_database_from_files(rootdir, engine)
