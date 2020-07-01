from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
import os


def get_engine_and_connection():
    # It allows to have multiple docker database containers and input different host port for container

    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    database = os.environ['POSTGRES_DB']
    port = input("Enter port for database connection: ")

    while True:
        try:
            engine = db.create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
            connection = engine.connect()
        except Exception as e:
            print(e)
        else:
            break
    return engine, connection


engine, connection = get_engine_and_connection()
Base = declarative_base()


class SampleRun(Base):
    __tablename__ = 'sample_run'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sample_id = db.Column(db.String(100))
    run_id = db.Column(db.String(100))
    variant_stats = db.orm.relationship('VariantStats', back_populates='sample_run', uselist=False)
    read_qc = db.orm.relationship('ReadQc', back_populates='sample_run', uselist=False)
    wgs_stats = db.orm.relationship('WGSstats', back_populates='sample_run', uselist=False)

    pipeline_type = db.Column(db.String(100))
    analysis_status = db.Column(db.String(100))
    genome_analysist = db.Column(db.String(100))
    mate_sample = db.Column(db.String(100))

    __table_args__ = (db.schema.UniqueConstraint('sample_id', 'run_id', name='_sample_run_sample_id_run_id_uc'),)

    def __repr__(self):
        return f'<SampleRun {self.sample_id} {self.run_id}>'


class VariantStats(Base):
    __tablename__ = 'variant_stats'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sample_run_id = db.Column(db.Integer, db.ForeignKey('sample_run.id'))
    sample_run = db.orm.relationship('SampleRun', back_populates='variant_stats')

    sample_id = db.Column(db.String(100))
    run_id = db.Column(db.String(100))

    num_variants = db.Column(db.Integer())
    num_hets = db.Column(db.Integer())
    num_hets_chrx = db.Column(db.Integer())

    __table_args__ = (db.schema.UniqueConstraint('sample_id', 'run_id', name='_variant_stats_sample_id_run_id_uc'),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<VariantStats {self.sample_id} {self.run_id}>'


class PipelineRuns(Base):
    __tablename__ = 'pipeline_runs'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sample_run_id = db.Column(db.Integer, db.ForeignKey("sample_run.id"))

    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    status = db.Column(db.String(100))
    location = db.Column(db.String(100))
    current_task = db.Column(db.String(100))
    pipeline_config = db.Column(db.String(100))

    def __repr__(self):
        return f'<PipelineRuns {self.id} {self.run_id} {self.status}>'


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer())
    run_id = db.Column(db.Integer, db.ForeignKey("pipeline_runs.id"))
    timestamp_start = db.Column(db.String(100))
    timestamp_end = db.Column(db.String(100))
    tool = db.Column(db.String(100))
    cmd = db.Column(db.String(100))
    requester = db.Column(db.String(100))
    status = db.Column(db.String(100))
    input = db.Column(db.String(100))
    output = db.Column(db.String(100))

    def __repr__(self):
        return f'<Job {self.id} {self.job_id} {self.run_id} {self.status}>'


class ResultFile(Base):
    __tablename__ = 'result_file'

    file_id = db.Column(db.Integer(), primary_key=True)
    sample_id = db.Column(db.String(100))
    filetype = db.Column(db.String(100))
    path = db.Column(db.String(100))
    file_format = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime())

    def __repr__(self):
        return f'<ResultFile {self.file_id} {self.sample_id}>'


class ReadQc(Base):
    __tablename__ = 'read_qc'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sample_run_id = db.Column(db.Integer, db.ForeignKey('sample_run.id'))
    sample_run = db.orm.relationship('SampleRun', back_populates='read_qc')

    sample_id = db.Column(db.String(100))
    run_id = db.Column(db.String(100))

    total = db.Column(db.Integer())
    secondary = db.Column(db.Integer())
    supplementary = db.Column(db.Integer())
    duplicates = db.Column(db.Integer())
    mapped = db.Column(db.Integer())
    paired = db.Column(db.Integer())
    read1 = db.Column(db.Integer())
    read2 = db.Column(db.Integer())
    properly_paired = db.Column(db.Integer())
    with_itself_and_mate_mapped = db.Column(db.Integer())
    singletons = db.Column(db.Integer())
    mq0 = db.Column(db.Integer())
    mq5 = db.Column(db.Integer())

    fastqc_r1 = db.Column(db.String(250))
    fastqc_r2 = db.Column(db.String(250))

    def __repr__(self):
        return f'<ReadQc {self.id} {self.sample_id}>'


class WGSstats(Base):
    __tablename__ = 'wgs_stats'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sample_run_id = db.Column(db.Integer, db.ForeignKey('sample_run.id'))
    sample_run = db.orm.relationship('SampleRun', back_populates='wgs_stats')

    sample_id = db.Column(db.String(100))
    run_id = db.Column(db.String(100))

    average_depth = db.Column(db.Float())
    percentage_above_10 = db.Column(db.Float())
    percentage_above_20 = db.Column(db.Float())
    percentage_above_30 = db.Column(db.Float())

    def __repr__(self):
        return f'<WGSstats {self.id} {self.sample_id} {self.run_id}>'


class WGSqc(Base):
    """
    gene_id: Gene symbol.
    transcript_id: Transcript symbol encoded by gene in gene_id.
    sample_id: Filename (eg. MNM00001).

    mean_cov: Mean coverage value for given transcript of a gene.
    percentage_above_10: Percent of a transcript covered at least by 10 reads.
    percentage_above_20: Percent of a transcript covered at least by 20 reads.
    percentage_above_30: Percent of a transcript covered at least by 30 reads.
    """

    __tablename__ = 'wgs_qc'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    gene_id = db.Column(db.String(32))
    transcript_id = db.Column(db.String(32), index=True)
    sample_id = db.Column(db.String(32), index=True)
    # run_id = db.Column(db.String(32))
    # sample_run = db.Column(db.String(64))

    mean_coverage = db.Column(db.Integer)
    percentage_above_10 = db.Column(db.Integer)
    percentage_above_20 = db.Column(db.Integer)
    percentage_above_30 = db.Column(db.Integer)


Base.metadata.create_all(engine)
