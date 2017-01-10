# ORMs for the database to store search for gene-drug associations.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Float, Binary
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from config import DATABASE
import math
import json


def init():
    # Following 3 lines taken from this resource:
    # http://xion.org.pl/2012/06/12/interesting-problem-with-mysql-sqlalchemy/
    class _Base(object):
        """Base class for SQLAlchemy model classes."""
        __table_args__ = {'mysql_engine': 'InnoDB'}

    engine = create_engine(DATABASE)
    Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    global session
    session = Session()

    # ORMs of the database
    Base = declarative_base(cls=_Base)

    global Signature
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

    global Association
    class Association(Base):
        __tablename__ = 'association'
        id = Column(Integer, primary_key=True)
        signature_fk = Column(Integer, ForeignKey('signature.id'))
        gene_symbol = Column(String(25))
        fold_change = Column(Float)
        p_value = Column(Float)

        def get_row(self):
            s = get_or_create(session, Signature, id=self.signature_fk)[0]
            sig_id = s.sig_id
            pert_id = s.pert_id
            drug_name = s.drug_name
            pert_time = s.pert_time
            pert_time_unit = s.pert_time_unit
            pert_dose = s.pert_dose

            return drug_name, \
                sig_id, \
                pert_id, \
                pert_time, \
                pert_time_unit, \
                pert_dose, \
                self.p_value, \
                self.fold_change


    global creedsSignature
    class creedsSignature(Base):
        __tablename__ = 'creeds_signature'
        id = Column(Integer, primary_key=True)
        drug_name = Column(String(50))
        geo_id = Column(String(50))
        drugbank_id = Column(String(50))
        pubchem_id = Column(String(50))
        associations = relationship('creedsAssociation')


    global creedsAssociation
    class creedsAssociation(Base):
        __tablename__ = 'creeds_association'
        id = Column(Integer, primary_key=True)
        signature_fk = Column(Integer, ForeignKey('creeds_signature.id'))
        gene_symbol = Column(String(25))
        p_value = Column(Float)
        fold_change = Column(Float)

        def get_row(self):
            cs = get_or_create(session, creedsSignature, id=self.signature_fk)[0]
            drug_name = cs.drug_name

            geo_id = cs.geo_id
            geo_url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + geo_id

            drugbank_id = cs.drugbank_id
            if drugbank_id is not None:  # Make sure to only add if it exists.
                drugbank_url = 'http://www.drugbank.ca/drugs/' + drugbank_id
            else:
                drugbank_url = None

            pubchem_id = cs.pubchem_id
            if pubchem_id is not None:
                pubchem_url = 'https://pubchem.ncbi.nlm.nih.gov/compound/' + pubchem_id
            else:
                pubchem_url = None

            return drug_name,\
                geo_id,\
                drugbank_id,\
                pubchem_id,\
                self.p_value,\
                self.fold_change,\
                geo_url,\
                drugbank_url,\
                pubchem_url

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


# This function performs error-checking on the user's gene symbol input.
def symbol_validate(symbol):
    # with open('static/js/array.json') as array:
    symbols = json.load(open('DGB/static/js/array.json', 'r'))
    return symbol in symbols
    #     return True
    # else:
    #     return False


# A function to split a list with at least 10 elements into deciles.
def decile_calculate(array):
    # Determine whether this list has negative values or positive values.
    positive = True
    if array[0] > 0:
        positive = True
    else:
        positive = False
        for each_item in array:
            negative_value = array.index(each_item)
            array[negative_value] *= -1
            array.sort()

    # Determine how to split a list of n-elements into 10 parts.
    guide = [0] * 10
    length = len(array)
    base = length/float(10)
    for num in xrange(0, 10):
        guide[num] = base * (num + 1)

    # Round the guide down to the next lowest whole number (we don't want fractional parts at all)
    # This tells us the indexes of the "elements" of the original list that should serve as the cutoffs for each decile.
    cutoffs = [0] * 10
    for entry in guide:
        index = guide.index(entry)
        cutoffs[index] = int(math.floor(guide[index]))

    # We must now create a list, replacing the index of the aforementioned "elements" with the "elements" themselves.
    decile_maxima = [0] * 10
    for num in xrange(0, 10):
        max_index = cutoffs[num] - 1
        decile_maxima[num] = array[max_index]
    decile_maxima.sort()

    deciles = []
    if positive:
        for list_item in array:
            counter = 0
            while list_item >= decile_maxima[counter]:
                if counter == 9:
                    counter += 1
                    break
                else:
                    counter += 1
            if counter == 0:
                deciles.append(1)
            else:
                deciles.append(counter)
        return deciles
    else:
        for list_item in array:
            counter = 0
            while list_item >= decile_maxima[counter]:
                if counter == 9:
                    counter += 1
                    break
                else:
                    counter += 1
            if counter == 0:
                deciles.append(1)
            else:
                deciles.append(counter)
        deciles.sort(reverse=True)

    return deciles


# This function will return a tuple; each entry of that tuple represents a row of the output table.
def lincs_rows(symbol, expression):

    init()
    association = get_or_create(session, Association, gene_symbol=symbol)
    total_count = association.count()
    associations = association[0:]
    rows = [None] * total_count

    for i in xrange(total_count):
        entry = associations[i]
        row = None
        if (expression == 'Up' and entry.fold_change > 0) or \
                (expression == 'Down' and entry.fold_change < 0):
            row = entry.get_row()
        rows[i] = row

    # Sort the lists in order of fold-change, and calculate decile scores for each association.
    rows = filter(None, rows)
    rows = sorted(rows, key=lambda tup: tup[7])
    length = len(rows)

    fold_changes = [0] * length
    for i in xrange(length):
        fold_changes[i] = rows[i][7]

    deciles = decile_calculate(fold_changes)

    # This will pass in a string to the output page, reminding the user of the option they chose (up vs down).
    if expression == 'Up':
        pattern = 'Up-Regulated'
    else:
        pattern = 'Down-Regulated'

    result = (rows, deciles, pattern)
    return result


def creeds_rows(symbol, expression):
    init()

    # Find all instances of the gene in the associations table.
    creedsassociation = get_or_create(session, creedsAssociation, gene_symbol=symbol)
    creedsassociations = creedsassociation[0:]
    total_count = creedsassociation.count()
    creedsrows = [None] * total_count

    for i in xrange(total_count):
        entry = creedsassociations[i]
        # This if statement ensures that we only extract the associations with desired expression patterns.
        row = None
        if (expression == 'Up' and entry.fold_change > 0) or \
                (expression == 'Down' and entry.fold_change < 0):
            row = entry.get_row()
        creedsrows[i] = row

    # Sort the lists in order of fold-change, and calculate decile scores for each association.
    creedsrows = filter(None, creedsrows)
    # creedsrows = sorted(creedsrows, key=lambda tup: tup[5])
    length = len(creedsrows)

    fold_changes = [0] * length
    for i in xrange(length):
        fold_changes[i] = creedsrows[i][5]

    deciles = decile_calculate(fold_changes)

    # This will pass in a string to the output page, reminding the user of the option they chose (up vs down).
    if expression == 'Up':
        pattern = 'Up-Regulated'
    else:
        pattern = 'Down-Regulated'

    result = (creedsrows, deciles, pattern)
    return result
