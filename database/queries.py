import sys
sys.path.append("..")
from database.base import Session
from collections import defaultdict
import time
import pandas as pd


def get_first_row_for_default(table_name: "Class"):
    """
    :param table_name:  Name of a table to get first row.
    :return: First row from table to use as default value.
    """
    session = Session()
    val = session.query(table_name) \
        .filter(table_name.id == 1) \
        .all()
    try:
        return val[0].gene_id
    except IndexError:  # If database is empty then val[0] returns IndexError
        return "None"


def get_all_transcripts_names(table_name: "Class", type: "String"):
    """
    :param table_name: Name of a table to get transcripts names.
    :param type: Output type. "object" for list of objects, "transcript_id" for list of transcripts ID's as strings.
    :return: List of all distinct record objects or attributes of this object.
    """
    session = Session()

    transcripts = session.query(table_name)\
                  .distinct(table_name.transcript_id)\
                  .all()

    session.close()

    if type == "object":
        return transcripts
    else:
        return [getattr(obj, type) for obj in transcripts]


def get_transcripts_by_gene(table_name: "Class", type: "String"):
    """
    :param table_name: Name of table to create dictionary from.
    :return: Dictionary of genes (keys) and lists of transcripts that they encode (values).
    """
    print("Querying...")
    start = time.perf_counter()
    distincts = get_all_transcripts_names(table_name, type=type)
    print(f"Query done, exec time {round(time.perf_counter() - start)} seconds")

    dropdown_options = defaultdict(list)
    for obj in distincts:
        dropdown_options[obj.gene_id].append(obj.transcript_id)

    return dropdown_options


def get_all_file_names(table_name: "Class", type: "String"):
    """
    :param table_name: Name of a table to get file names.
    :return: List of all distinct record objects or strings of sample_id's.
    """
    session = Session()

    files = session.query(table_name)\
            .distinct(table_name.sample_id)\
            .all()

    session.close()

    if type == "object":
        return files
    else:
        return [getattr(obj, type) for obj in files]


def get_stats_for_plot(table_name, transcript, gene, stat, sample_ids=False):
    """
    Allows user to pass wanted transcript ID, gene ID and statistics (one from following: "mean_cov",
    "cov_10", "cov_20", "cov_30") and returns pd.DataFrame object with one or two columns (depends
    if user wants corresponding statistics with sample ID's or not) of corresponding statistics for
    matching gene and transcript.

    :param table_name: Name of a table to get stats (eg. Record).
    :param transcript: Transcript selected in dropdown.
    :param gene: Gene selected in dropdown.
    :param stat: Statistics to return (eg. "mean_cov").
    :param samle_ids: True if function should return additional column with sample ID's.
    :return: Pandas dataframe object of wanted statistic values in all samples for given transcript and gene.
    """
    session = Session()

    values = session.query(table_name)\
             .filter(table_name.transcript_id == transcript)\
             .filter(table_name.gene_id == gene)\
             .all()

    session.close()

    sample_id_list = [obj.sample_id for obj in values]
    statistics_values = [getattr(obj, stat) for obj in values]

    if sample_ids:
        return pd.DataFrame(list(zip(statistics_values, sample_id_list)), columns=["value", "id"])
    else:
        return pd.DataFrame(statistics_values, columns=["value"])


def get_stats_for_one_sample(table_name, sample, transcript, gene, stat):
    """
    Sample highlighting handler. Allows user to pass transcript ID, gene ID, sample ID and
    statistics (one from following: "mean_cov", "cov_10", "cov_20", "cov_30") and returns
    value for specified statistics for transcript of a specified gene from specified sample.

    :param table_name: Name of a table to get stats (eg. Record).
    :param sample: Sample to highlight selected in radiobox.
    :param transcript: Transcript selected in dropdown.
    :param gene: Gene selected in dropdown.
    :param stat: Statistics to return (eg. "mean_cov").
    :return: Value of satistics
    """

    session = Session()

    stats = session.query(table_name)\
            .filter(table_name.sample_id == sample) \
            .filter(table_name.transcript_id == transcript) \
            .filter(table_name.gene_id == gene)\
            .all()

    session.close()

    try:
        stat = getattr(stats[0], stat)
    except IndexError:
        return ""

    return stat
