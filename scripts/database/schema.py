from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# new database that combines old databases, and will be updated with the latest data
SUMMARY_DATABASE_PATH = "sqlite:///../../summary_data/bacteria_data.db"
"""
  The database schema for the new bacteria summary database
"""

Base = declarative_base()
# Create the database schema
class Species(Base):
  __tablename__ = "species"
  # reference: Mangul_Lab_USC/db.microbiome/Bacteria/bacteria_data.db
  id = Column(Integer, primary_key=True)
  given_taxid = Column(Integer)
  genus_taxid = Column(Integer)
  species_taxid = Column(Integer)
  dbmane = Column(String)
  # additional columns from the other bacteria database
  filename = Column(String)
  # path to the file on discovery filesystem
  file_path = Column(String)

  def __rept__(self):
    return "<DatabaseEntry (given_taxid=%d, genus_taxid=%d, species_taxid=%d, dbname='%s')>" % (
      self.given_taxid,
      self.genus_taxid,
      self.species_taxid,
      self.dbname
    )

# TODO: Are these necessary for our study?
# rather than make two databases we will compile all the data onto one but on multiple tables
class ChromosomeStats(Base):
  __tablename__ = "species_chromosome_stats"
  
  id = Column(Integer, primary_key=True)
  species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
  chromosome_count = Column(Integer, default=0)
  avg_chromosome_length = Column(Integer)
  max_chromosome_length = Column(Integer)
  min_chromosome_length = Column(Integer)


class PlasmidStats(Base):
  __tablename__ = "species_plasmid_stats"

  id = Column(Integer, primary_key=True)
  species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
  plasmid_count = Column(Integer, default=0)
  avg_plasmid_length = Column(Integer)
  max_plasmid_length = Column(Integer)
  min_plasmid_length = Column(Integer)


class ContigStats(Base):
  __tablename__ = "species_contig_stats"

  id = Column(Integer, primary_key=True)
  species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
  contig_count = Column(Integer, default=0)
  avg_contig_length = Column(Integer)
  max_contig_length = Column(Integer)
  min_contig_length = Column(Integer)


def create_database():
  """"
    Creates the database schema for the new bacteria summary database
  """

  engine = create_engine(SUMMARY_DATABASE_PATH, echo=True)
  # push the exiting schema to the database
  Base.metadata.create_all(engine)
  session = sessionmaker(bind=engine)()
  session.commit()

def database_session():
  engine = create_engine(SUMMARY_DATABASE_PATH, echo=True)
  return sessionmaker(bind=engine)()
