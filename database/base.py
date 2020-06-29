#!/bin/python3

from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
database = os.environ['POSTGRES_DB']

# Connection with postgres database in Docker container
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
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

    id = Column(Integer, primary_key=True)

    transcript_id = Column(String, index=True)
    sample_id = Column(String, index=True)
    gene_id = Column(String)

    mean_cov = Column(Float)

    cov_10 = Column(Float)
    cov_20 = Column(Float)
    cov_30 = Column(Float)

    def __init__(self, transcript_id, sample_id, gene_id, mean_cov, cov_10, cov_20, cov_30):
        self.transcript_id = transcript_id
        self.sample_id = sample_id
        self.gene_id = gene_id
        self.mean_cov = mean_cov
        self.cov_10 = cov_10
        self.cov_20 = cov_20
        self.cov_30 = cov_30