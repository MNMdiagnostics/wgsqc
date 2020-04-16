from base import Session, engine, Base, Record

Base.metadata.create_all(bind=engine)

session = Session()

record = Record(1, "NR_046018.2", "MNM00001", "DDX11L1", 53.27, 96.85, 92.62, 86.26)

session.add(record)
session.commit()

