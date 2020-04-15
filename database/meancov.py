from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship, backref

from database.base import Base


class Gene(Base):
    __tablename__ = 'gene'
    gene_id = Column(String, primary_key=True)
    mean_cov = Column(Float)
    gene = relationship()

    def __init__(self, mean_cov):
        self.mean_cov = mean_cov
