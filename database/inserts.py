from base import Session, engine, Base, Record
import pandas as pd
import sys
import os
import time
import statistics


def add_to_database_from_files(root_directory):
    """
    Adds records to database from nested directory of a tab separated files.

    :param root_directory: Path to directory containing subdirectories with files.
    :param base:
    """
    colnames = ("transcript_id", "gene_id", "mean_cov", "cov_10", "cov_20", "cov_30")
    Base.metadata.create_all(bind=engine)
    total = time.perf_counter()
    times = []
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            print("CURRENT FILE:", file)
            t = time.perf_counter()
            file_absolute_path = os.path.join(subdir, file)
            table = pd.read_csv(file_absolute_path, sep="\t", header=None, names=colnames)
            table['sample_id'] = os.path.basename(subdir)
            table.to_sql('record', engine, if_exists='append', index=False)
            print(f"FILE {file} ADDED TO DATABASE, EXECUTION TIME: {time.perf_counter() - t}")
            times.append(time.perf_counter() - t)
    print(f"\n\nTOTAL TIME: {time.perf_counter() - total}")
    print(f"MAX TIME: {max(times)}")
    print(f"MIN TIME: {min(times)}")
    print(f"MEAN TIME: {statistics.mean(times)}")


if __name__ == "__main__":
    # READ FROM FILES
    if len(sys.argv) == 2:
        rootdir = sys.argv[1]
    elif len(sys.argv) == 1:
        print("Root directory set up as /home/username")
        rootdir = "~/"
    add_to_database_from_files(rootdir)