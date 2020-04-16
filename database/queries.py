from base import Session, Record

session = Session()

tmp = session.query(Record).all()

for t in tmp:
    print(t.transcript_id)

session.close()