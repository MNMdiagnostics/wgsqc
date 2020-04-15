from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Gene(Base):
    __tablename__ = 'gene'

    transcript_id = Column(String, primary_key=True)
    gene_id = Column(String)

    def __init__(self, gene_id):
        self.gene_id = gene_id
