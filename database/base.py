#!/bin/python3

# transcript - gene: one-to-one
# gene - meancov: one-to-many
# gene - cov10: one-to-many
# gene - cov20: one-to-many
# gene - cov30: one-to-many
# https://dbdiagram.io/d/5e96c35b39d18f5553fda003

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
Session = sessionmaker(bind=engine)
Base = declarative_base()
