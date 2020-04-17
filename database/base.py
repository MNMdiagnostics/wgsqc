#!/bin/python3

from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection with postgres database in Docker container
engine = create_engine(r'postgresql+psycopg2://test_user:test@localhost:5432/test_name')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Record(Base):
    """
    Database table

    transcript_id: Transcript symbol.
    sample_id: Name of a file data come from.
    gene_id: Gene symbol encoding transcript in transcript_id.
    mean_cov: Mean coverage value for given transcript of a gene.
    cov_10: Percent of a transcript covered at least 10 X.
    cov_20: Percent of a transcript covered at least 20 X.
    cov_33: Percent of a transcript covered at least 30 X.
    transcript_sample: Unique identifier of a single record <sample_id>_<transcript_id> (eg. MNM00001_NR_046018.2)
    """
    __tablename__ = 'record'

    transcript_id = Column(String)
    sample_id = Column(String)
    gene_id = Column(String)
    mean_cov = Column(Float)
    cov_10 = Column(Float)
    cov_20 = Column(Float)
    cov_30 = Column(Float)
    transcript_sample = Column(String, primary_key=True)

    def __init__(self, transcript_id, sample_id, gene_id, mean_cov, cov_10, cov_20, cov_30, transcript_sample):
        self.transcript_id = transcript_id
        self.sample_id = sample_id
        self.gene_id = gene_id
        self.mean_cov = mean_cov
        self.cov_10 = cov_10
        self.cov_20 = cov_20
        self.cov_30 = cov_30
        self.transcript_sample = transcript_sample
