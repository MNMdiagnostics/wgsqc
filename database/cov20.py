from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship, backref

from database.base import Base


class Cov20(Base):
    __tablename__ = 'cov20'
    gene_id = Column(String, primary_key=True)
    cov_20 = Column(Float)
    gene = relationship()

    def __init__(self, cov_20):
        self.mean_cov = cov_20
