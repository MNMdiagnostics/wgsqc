from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship, backref

from database.base import Base


class Cov10(Base):
    __tablename__ = 'cov10'
    gene_id = Column(String, primary_key=True)
    cov_10 = Column(Float)
    gene = relationship()

    def __init__(self, cov_10):
        self.mean_cov = cov_10
