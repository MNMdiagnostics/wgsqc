#!/bin/python3

from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Record(Base):
    __tablename__ = 'record'

    transcript_id = Column(String, primary_key=True)
    sample_id = Column(String)
    gene_id = Column(String)
    mean_cov = Column(Float)
    cov_10 = Column(Float)
    cov_20 = Column(Float)
    cov_30 = Column(Float)


engine = create_engine("postgresql:///records.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()
record = Record()

record.transcript_id = "NR_046018.2"
record.sample_id = "MNM00001"
record.gene_id = "DDX11L1"
record.mean_cov = 53.27
record.cov_10 = 96.85
record.cov_20 = 92.62
record.cov_30 = 86.26

session.close()