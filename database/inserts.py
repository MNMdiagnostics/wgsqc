from base import Session, engine, Base, Record
from queries import get_all_distincts
import pandas as pd
import sys
import os


def add_to_database_from_files(root_directory):
    """
    Adds records to database from nested directory of a tab separated files.

    :param root_directory: Path to directory containing subdirectories with files.
    """

    colnames = ("transcript_id", "gene_id", "mean_cov", "cov_10", "cov_20", "cov_30")
    Base.metadata.create_all(bind=engine)

    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            file_absolute_path = os.path.join(subdir, file)
            filename = os.path.basename(subdir)
            table = pd.read_csv(file_absolute_path, sep="\t", header=None, names=colnames)

            transcripts_from_current_database = get_all_distincts(Record, "transcript_id", "transcript_id")
            transcripts_from_current_file = table.transcript_id.unique()

            in_database_but_not_in_file = [transcript for transcript in transcripts_from_current_database if
                                           transcript not in transcripts_from_current_file]

            in_file_but_not_in_database = [transcript for transcript in transcripts_from_current_file if
                                           transcript not in transcripts_from_current_database]

            session = Session()
            for id, row in table.iterrows():
                control_print(id, filename)

                if in_database_but_not_in_file:
                    null_record(in_database_but_not_in_file, row, filename, session)

                elif in_file_but_not_in_database:
                    null_transcripts_to_existing_records(in_file_but_not_in_database, session)

                else:
                    session.add(normal_record(row, filename))

            session.commit()
            print(f"FILE {file} ADDED TO DATABASE\n")


def normal_record(row, filename):
    """
    Adds normal record to database. Case when database is empty or transcript is known in database.

    :param row: Single row of given file.
    :param filename: Name of a file, stored in database as sample ID.
    :return: Record object to be added to database.
    """
    transcript_sample = filename + "_" + row['transcript_id']
    record = Record(row['transcript_id'],
                    filename,
                    row['gene_id'],
                    row['mean_cov'],
                    row['cov_10'],
                    row['cov_20'],
                    row['cov_30'],
                    transcript_sample
                    )
    return record


def null_record(in_database_but_not_in_file, row, filename, session):
    """
    Handler for case, when transcript present in database is not present in current file.

    :param in_database_but_not_in_file: List of transcripts present in database but not in current file.
    :param row: Single row of given file.
    :param filename: Name of a file, stored in database as sample ID.
    :param session: Current session object.
    """
    transcript_sample = filename + "_" + row['transcript_id']
    for transcript in in_database_but_not_in_file:
        record = Record(transcript,
                        filename,
                        "NULL",
                        "NULL",
                        "NULL",
                        "NULL",
                        "NULL",
                        transcript_sample)
        session.add(record)


def null_transcripts_to_existing_records(in_file_but_not_in_database, session):
    """
    Handler for case, when transcript present in current file is not present in database.

    :param in_file_but_not_in_database: List of transcripts present in file but not in database.
    :param session: Current session object.
    """
    samples_from_current_database = get_all_distincts(Record, "sample_id", "sample_id")
    for transcript in in_file_but_not_in_database:
        for sample in samples_from_current_database:
            transcript_sample = sample + "_" + transcript
            record = Record(
                transcript,
                sample,
                "NULL",
                "NULL",
                "NULL",
                "NULL",
                "NULL",
                transcript_sample)
            session.add(record)


def control_print(id, filename):
    """
    Prints information for user every 50k rows when inserting files.

    :param id: Current row number.
    :param filename: Current file name.
    """
    if id % 50_000 == 0:
        print(f"FILE {filename}, ROW: {id}")


if __name__ == "__main__":
    # READ FROM FILES
    if len(sys.argv) == 2:
        rootdir = sys.argv[1]
    elif len(sys.argv) == 1:
        rootdir = "~/"
    add_to_database_from_files(rootdir)
