from base import Session, engine, Base, Record
from database.queries import get_all_transcripts_names, get_all_file_names
import pandas as pd
import sys
import os


def add_to_database_from_files(root_directory: 'String, commandline argument'):
    """
    Adds records to database from nested directory of a tab separated files.

    :param root_directory: Path to directory containing subdirectories with files.
    """

    colnames = ("transcript_id", "gene_id", "mean_cov", "cov_10", "cov_20", "cov_30")
    Base.metadata.create_all(bind=engine)

    # GET ALL TRANSCRIPTS NAMES PRESENT IN CURRENT DATABASE
    current_transcripts = get_all_transcripts_names(Record, "transcript_id")

    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            print("CURRENT FILE:", file)
            file_absolute_path = os.path.join(subdir, file)
            sample_id = os.path.basename(subdir)
            table = pd.read_csv(file_absolute_path, sep="\t", header=None, names=colnames)
            transcripts_from_table = list(table["transcript_id"].unique())

            transcript_absence_in_file_handler(current_transcripts, transcripts_from_table, sample_id)

            for id, row in table.iterrows():
                # CONTROL PRINT
                if id % 50_000 == 0:
                    print("ROW:", id)

                transcript_sample = sample_id + "_" + row['transcript_id']
                session = Session()
                if current_transcripts and row['transcript_id'] not in current_transcripts:
                    # CREATE RECORDS FOR THIS TRANSCRIPT IN PREVIOUS SAMPLES, IF
                    # THIS IS FIRST OCCURRENCE AND DATABASE CONTAINS PREVIOUS SAMPLES
                    all_files_in_database = get_all_file_names(Record, "sample_id")
                    for filename in all_files_in_database:
                        record = Record(row['transcript_id'],
                                        filename,
                                        "NULL",
                                        "NULL",
                                        "NULL",
                                        "NULL",
                                        "NULL",
                                        transcript_sample,
                                        )
                        session.add(record)
                else:
                    record = Record(row['transcript_id'],
                                    sample_id,
                                    row['gene_id'],
                                    row['mean_cov'],
                                    row['cov_10'],
                                    row['cov_20'],
                                    row['cov_30'],
                                    transcript_sample
                                    )
                    session.add(record)
                session.commit()
            print(f"FILE {file} ADDED TO DATABASE\n")


def transcript_absence_in_file_handler(current_transcripts: 'List of strings',
                                       transcripts_from_table: 'List of strings',
                                       sample_id: 'String'):
    """
    :param current_transcripts: Transcripts present in database.
    :param transcripts_from_table: Transcripts present in current file.
    :param sample_id: Sample identifier.
    """
    record_to_add = [row for row in current_transcripts if
                     row not in transcripts_from_table]

    for transcript_id in record_to_add:
        session = Session()
        session.add(Record(transcript_id, sample_id, "NULL", "NULL", "NULL", "NULL", "NULL",
                           transcript_id + "_" + sample_id))
        session.commit()
        print(f"ADDED {transcript_id} WITH NULL VALUES, BECAUSE WAS ABSENT IN CURRENT FILE")


if __name__ == "__main__":
    # READ FROM FILES
    if len(sys.argv) == 2:
        rootdir = sys.argv[1]
    elif len(sys.argv) == 1:
        rootdir = "~/"
    add_to_database_from_files(rootdir)