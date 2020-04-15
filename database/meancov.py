from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from database.base import Base


class Meancov(Base):
    __tablename__ = 'meancov'
    gene_id = Column(String, primary_key=True)
    mean_cov = Column(Float)
    gene = relationship()

    def __init__(self, mean_cov):
        self.mean_cov = mean_cov
