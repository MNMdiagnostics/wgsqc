import sys
sys.path.append("..")
from database.base import Session
from collections import defaultdict


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

    distincts = get_all_transcripts_names(table_name, type=type)

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

