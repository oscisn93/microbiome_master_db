from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, mapper, Session

# copies of the old databases from original paper/project
OLD_SUMMARY_PATH = "sqlite:///../summary_data/old_db/bacteria_summary.db"
OLD_DATABASE_PATH = "sqlite:///../summary_data/old_db/bacteria_data.db"


"""
  The database schemas for the old bacteria summary databases
"""


class Species(object):
  pass


class SpeciesStats(object):
  pass


# Because the databases did not contain primary keys, we will have to create them
# manually. This reference is helpfule: https://docs.sqlalchemy.org/en/14/core/constraints.html#primary-key-constraint


def database_session() -> Session:
  """"
    Creates the database schema/mapper for bacteria_data.db
  """
  engine_database = create_engine(OLD_DATABASE_PATH, echo=True)
  metadata_database = MetaData(engine_database)
  species_stats = Table("SPECIESDB", metadata_database,
                        Column("dbname".upper(), String),
                        Column("filename".upper(), String),
                        Column("filepath".upper(), String),
                        Column("chromosome_count", Integer),
                        Column("avg_length_chromosomes", Integer),
                        Column("max_length_chromosomes", Integer),
                        Column("min_length_chromosomes", Integer),
                        Column("plasmid_count", Integer),
                        Column("avg_length_plasmids", Integer),
                        Column("max_length_plasmids", Integer),
                        Column("min_length_plasmids", Integer),
                        Column("contig_count", Integer),
                        Column("avg_length_contig", Integer),
                        Column("max_length_contig", Integer),
                        Column("min_length_contig", Integer),
                        PrimaryKeyConstraint("dbname".upper(), "filename".upper(), name="pk_speciesdb"),
  )
  mapper(SpeciesStats, species_stats)
  return sessionmaker(bind=engine_database)()


def summary_session() -> Session:
  """"
    Creates the database schema/mapper for bacteria_summary.db
  """
  engine_summary = create_engine(OLD_SUMMARY_PATH, echo=True)
  metadata_summary = MetaData(engine_summary)
  species = Table("BACT_DB", metadata_summary,
                  Column("giventaxid".upper(), Integer),
                  Column("genustaxid".upper(), Integer),
                  Column("speciestaxid".upper(), Integer),
                  Column("dbname".upper(), String),
                  PrimaryKeyConstraint("giventaxid".upper(), "genustaxid".upper(), "speciestaxid".upper(), name="pk_id"),
                  autoload=True
  )
  mapper(Species, species)
  return sessionmaker(bind=engine_summary)()
