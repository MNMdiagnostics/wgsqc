from base import Session, Record

session = Session()

tmp = session.query(Record).all()

print(tmp)

session.close()