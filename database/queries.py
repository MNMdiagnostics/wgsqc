import sys
sys.path.append("..")
from database.base import Session
from collections import defaultdict


def get_all_distincts(table_name: "Class", type: "String", column: "String"):
    """
    :param table_name: Name of a table to get transcripts names.
    :param type: Output type. "object" for list of objects, "<attribute_name>" for list of attribute values as a strings.
    :param column: Column to get distinct values.
    :return: List of all distinct record objects or attributes of this object.

    get_all_distincts(Record, "object", "transcript_id") -> all distinct transcript ID's as list of objects
    get_all_distincts(Record, "sample_id", "sample_id") -> all distinct sample ID's as list of sample_id strings
    """

    session = Session()

    distincts = session.query(table_name) \
                .distinct(getattr(table_name, column)) \
                .all()

    session.close()

    if type == "object":
        return distincts
    else:
        return [getattr(obj, type) for obj in distincts]


def get_transcripts_by_gene(table_name: "Class", type: "String", column: "String"):
    """
    :param table_name: Name of table to create dictionary from.
    :param type: Output type. "object" for list of objects, "<attribute_name>" for list of attribute values as a strings.
    :param column: Column to get distinct values.
    :return: Dictionary of genes (keys) and lists of transcripts that they encode (values).
    """
    session = Session()

    distincts = get_all_distincts(table_name, type=type, column=column)

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

