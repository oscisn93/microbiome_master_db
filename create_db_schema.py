from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker


# Create the database
engine = create_engine("sqlite:///bacteria_data.db", echo=True)
# base class for our models
Base = declarative_base()


# each entry is one of the databases is a its own row
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


# rather than make two databases we will compile all the data onto one but on multiple tables
class SpeciesChromosomeStats(Base):
  __tablename__ = "species_chromosome_stats"
  
  id = Column(Integer, primary_key=True)
  species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
  chromosome_count = Column(Integer, default=0)
  avg_chromosome_length = Column(Integer)
  max_chromosome_length = Column(Integer)
  min_chromosome_length = Column(Integer)


class SpeciesPlasmidStats(Base):
  __tablename__ = "species_plasmid_stats"

  id = Column(Integer, primary_key=True)
  species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
  plasmid_count = Column(Integer, default=0)
  avg_plasmid_length = Column(Integer)
  max_plasmid_length = Column(Integer)
  min_plasmid_length = Column(Integer)


class SpeciesContigStats(Base):
  __tablename__ = "species_contig_stats"

  id = Column(Integer, primary_key=True)
  species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
  contig_count = Column(Integer, default=0)
  avg_contig_length = Column(Integer)
  max_contig_length = Column(Integer)
  min_contig_length = Column(Integer)


# push the schema onto the database.
# this will create the database if it does not exist
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
session.commit()
