from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

from database.base import Base


class Gene(Base):
    __tablename__ = 'gene'
    transcript_id = Column(String, primary_key=True)
    gene_id = Column(String)
    transcript = relationship("Transcript", backref=backref("gene", uselist=False))

    def __init__(self, gene_id):
        self.gene_id = gene_id
