from base import Session, engine, Base, Record
import pandas as pd
import sys
import os


def add_to_database_from_files(root_directory):
    """
    Adds records to database from nested directory of a tab separated files.

    :param root_directory: Path to directory containing subdirectories with files.
    :param base:
    """
    colnames = ("transcript_id", "gene_id", "mean_cov", "cov_10", "cov_20", "cov_30")
    Base.metadata.create_all(bind=engine)
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            session = Session()
            print("CURRENT FILE:", file)
            file_absolute_path = os.path.join(subdir, file)
            sample_id = os.path.basename(subdir)
            table = pd.read_csv(file_absolute_path, sep="\t", header=None, names=colnames)
            for id, row in table.iterrows():
                if id % 50_000 == 0:
                    print("ROW:", id)
                transcript_sample = sample_id + "_" + row['transcript_id']
                record = Record(row['transcript_id'], sample_id, row['gene_id'], row['mean_cov'], row['cov_10'], row['cov_20'], row['cov_30'], transcript_sample)
                session.add(record)
            session.commit()
            print(f"FILE {file} ADDED TO DATABASE\n")


if __name__ == "__main__":
    # READ FROM FILES
    if len(sys.argv) == 2:
        rootdir = sys.argv[1]
    elif len(sys.argv) == 1:
        rootdir = "~/"
    add_to_database_from_files(rootdir)