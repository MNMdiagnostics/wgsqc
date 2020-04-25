import sys
sys.path.append("..")
from database.base import Session
from collections import defaultdict
import time
import pprint


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
    session = Session()

    print("Querying...")
    start = time.time()
    distincts = get_all_transcripts_names(table_name, type=type)
    diff = time.time() - start
    print(f"Query done, exec time {diff} seconds")

    dropdown_options = defaultdict(list)
    for obj in distincts:
        dropdown_options[obj.gene_id].append(obj.transcript_id)

    session.close()
    return dropdown_options


def get_all_file_names(table_name: "Class", type: "String"):
    """
    :param table_name: Name of a table to get file names.
    :return: List of all distinct record objects or sample_id's of this objects.
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


def get_stats_for_plot(table_name, transcript, gene, stat):
    """
    :param table_name: Name of a table to get stats (eg. Record).
    :param transcript: Transcript symbol to filter.
    :param gene: Gene symbol to filter.
    :param stat: Statistics to return (eg. mean_cov).
    :return: List of wanted statistic values in all samples for given transcript and gene.
    """
    session = Session()

    values = session.query(getattr(table_name, stat))\
             .filter(table_name.transcript_id == transcript)\
             .filter(table_name.gene_id == gene)\
             .all()

    session.close()
    return [x[0] for x in values]
