from sqlalchemy import Column, String

from database.base import Base


class Transcript(Base):
    __tablename__ = 'transcript'
    transcript_id = Column(String, primary_key=True)
