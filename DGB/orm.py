# ORMs for the database to store search for gene-drug associations.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


# Following 3 lines taken from this resource: http://xion.org.pl/2012/06/12/interesting-problem-with-mysql-sqlalchemy/
class _Base(object):
    """Base class for SQLAlchemy model classes."""
    __table_args__ = {'mysql_engine': 'InnoDB'}

engine = create_engine('mysql://Kevin:Kevin@127.0.0.1:3306/creeds')
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# ORMs of the database
Base = declarative_base(cls=_Base)


class Signature(Base):
    __tablename__ = 'signature'
    id = Column(Integer, primary_key=True)
    sig_id = Column(String(50))
    pert_id = Column(String(20))
    drug_name = Column(String(50))
    pert_time = Column(Integer)
    pert_time_unit = Column(String(6))
    pert_dose = Column(Float)
    pert_dose_unit = Column(String(6))
    associations = relationship('Association')


class Association(Base):
    __tablename__ = 'association'
    id = Column(Integer, primary_key=True)
    signature_fk = Column(Integer, ForeignKey('signature.id'))
    gene_symbol = Column(String(25))
    fold_change = Column(Float)
    p_value = Column(Float)


class creedsSignature(Base):
    __tablename__ = '(creeds)signature'
    id = Column(Integer, primary_key=True)
    drug_name = Column(String(50))
    geo_id = Column(String(50))
    drugbank_id = Column(String(50))
    pubchem_id = Column(String(50))
    associations = relationship('creedsAssociation')


class creedsAssociation(Base):
    __tablename__ = '(creeds)association'
    id = Column(Integer, primary_key=True)
    signature_fk = Column(Integer, ForeignKey('(creeds)signature.id'))
    gene_symbol = Column(String(25))
    p_value = Column(Float)
    fold_change = Column(Float)


Base.metadata.create_all(engine)


# functions to add and retrieve objects
# This get_or_create is different from the one used in 6-13-16 because it obtains all instances, not just the first one.
def get_or_create(session, model, **kwargs):
    # init a instance if not exists
    # http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    instance = session.query(model).filter_by(**kwargs)
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


# This function will return a tuple; each entry of that tuple represents a row of the output table.
def lincs_rows(symbol, expression):
    # Below, we create empty lists that we will populate with the cells of the table.
    drug_names = []
    sig_ids = []
    pert_ids = []
    pert_times = []
    pert_time_units = []
    pert_doses = []
    p_values = []
    fold_changes = []

    # Find all instances of the gene in the associations table.
    association = get_or_create(session, Association, gene_symbol=symbol)
    for entry in association:
        # This if statement ensures that we only extract the associations with the desired expression patterns.
        if (expression == 'Up' and entry.fold_change > 0) or (expression == 'Down' and entry.fold_change < 0):
            # Here, we use the foreign key to access the relevant signature for each association.
            signature_fk = entry.signature_fk
            signature = get_or_create(session, Signature, id=signature_fk)

            # Iteratively populate the lists representing each column in the table.
            drug_names.append(signature[0].drug_name)
            sig_ids.append(signature[0].sig_id)
            pert_ids.append(signature[0].pert_id)
            pert_times.append(signature[0].pert_time)
            pert_time_units.append(signature[0].pert_time_unit)
            pert_doses.append(signature[0].pert_dose)
            p_values.append(entry.p_value)
            fold_changes.append(entry.fold_change)

    # This packages each of the relevant parts into each row.
    rows = zip(drug_names, sig_ids, pert_ids, pert_times,
               pert_time_units, pert_doses, p_values, fold_changes)

    # This will pass in a string to the output page, reminding the user of the option they chose (up vs down).
    if expression == 'Up':
        pattern = 'Up-Regulated'
    else:
        pattern = 'Down-Regulated'

    # Sort the output by fold-change.  We use reverse when they are negative as a proxy for absolute value.
    if expression == 'Up':
        rows = sorted(rows, key=lambda tup: tup[7], reverse=True)
    else:
        rows = sorted(rows, key=lambda tup: tup[7], reverse=False)

    result = (rows, pattern)
    return result


# This is just like the function above, but it queries the CREEDS tables rather than the L1000 ones.
def creeds_rows(symbol, expression):
    # Below, we create empty lists that we will populate with the cells of the table.
    # The lists that are labelled "..._urls" hold URLs so we can hyperlink to metadata pages.
    creeds_drug_names = []
    geo_ids = []
    geo_urls = []
    drugbank_ids = []
    drugbank_urls = []
    pubchem_ids = []
    pubchem_urls = []
    creeds_p_values = []
    creeds_fold_changes = []

    # Find all instances of the gene in the associations table.
    creedsassociation = get_or_create(session, creedsAssociation, gene_symbol=symbol)
    for entry in creedsassociation:
        # This if statement ensures that we only extract the associations with desired expression patterns.
        if (expression == 'Up' and entry.fold_change > 0) or \
                (expression == 'Down' and entry.fold_change < 0):
            # Here, we use the foreign key to access the relevant signature for each association.
            signature_fk = entry.signature_fk
            creedssignature = get_or_create(session, creedsSignature, id=signature_fk)

            # Iteratively populate the lists representing each column in the table.
            creeds_drug_names.append(creedssignature[0].drug_name)

            geo_ids.append(creedssignature[0].geo_id)
            geo_url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + creedssignature[0].geo_id
            geo_urls.append(geo_url)

            drugbank_ids.append(creedssignature[0].drugbank_id)

            if creedssignature[0].drugbank_id is not None:  # Make sure to only add if it exists.
                drugbank_url = 'http://www.drugbank.ca/drugs/' + creedssignature[0].drugbank_id
                drugbank_urls.append(drugbank_url)
            else:
                drugbank_url = None
                drugbank_urls.append(drugbank_url)

            pubchem_ids.append(creedssignature[0].pubchem_id)
            if creedssignature[0].pubchem_id is not None:
                pubchem_url = 'https://pubchem.ncbi.nlm.nih.gov/compound/' + creedssignature[0].pubchem_id
                pubchem_urls.append(pubchem_url)
            else:
                pubchem_url = None
                pubchem_urls.append(pubchem_url)

            creeds_p_values.append(entry.p_value)
            creeds_fold_changes.append(entry.fold_change)

    # This packages each of the relevant parts into each row.
    creedsrows = zip(creeds_drug_names, geo_ids, drugbank_ids, pubchem_ids,
                     creeds_p_values, creeds_fold_changes, geo_urls, drugbank_urls, pubchem_urls)

    # This will pass in a string to the output page, reminding the user of the option they chose (up vs down).
    if expression == 'Up':
        pattern = 'Up-Regulated'
    else:
        pattern = 'Down-Regulated'

    # Sort the output by fold-change.  We use reverse when they are negative as a proxy for absolute value.
    if expression == 'Up':
        creedsrows = sorted(creedsrows, key=lambda tup: tup[5], reverse=True)
    else:
        creedsrows = sorted(creedsrows, key=lambda tup: tup[5], reverse=False)

    result = (creedsrows, pattern)
    return result
