from database.old_schemas import database_session, summary_session, Species, SpeciesStats

# example usage of the databases
if __name__ == "__main__":
    summary = summary_session()
    database = database_session()

    species = summary.query(Species).all()
    summary.close()

    species_stats = database.query(SpeciesStats).all()
    database.close()

    print("species: %d" % len(species))
    print("species_stats: %d" % len(species_stats))
