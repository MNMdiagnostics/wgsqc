from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship, backref

from database.base import Base


class Cov30(Base):
    __tablename__ = 'cov30'
    gene_id = Column(String, primary_key=True)
    cov_30 = Column(Float)
    gene = relationship()

    def __init__(self, cov_30):
        self.mean_cov = cov_30
