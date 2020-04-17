import sys
sys.path.append("..")
from database.base import Session, Record
from collections import defaultdict


def get_transcripts_by_gene(table_name):
    """
    :param table_name: Name of table to create dictionary from.
    :return: Dictionary of genes (keys) and lists of transcripts that they encode (values).
    """
    session = Session()

    distincts = session.query(table_name)\
            .distinct(Record.transcript_id)\
            .all()

    dropdown_options = defaultdict(list)
    for obj in distincts:
        dropdown_options[obj.gene_id].append(obj.transcript_id)

    session.close()
    return dropdown_options