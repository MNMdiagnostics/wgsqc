from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

from database.base import Base


class Gene(Base):
    __tablename__ = 'gene'
    transcript_id = Column(String, primary_key=True)
    gene_id = Column(String)
    transcript = relationship("Transcript", backref=backref("gene", uselist=False))
    meancov = relationship("Meancov")
    cov_10 = relationship("Cov_10")
    cov_20 = relationship("Cov_20")
    cov_30 = relationship("Cov_30")

    def __init__(self, gene_id):
        self.gene_id = gene_id
