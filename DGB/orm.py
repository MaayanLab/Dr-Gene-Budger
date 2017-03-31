# ORMs for the database to store search for gene-drug associations.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Float, Binary
from sqlalchemy.orm import relationship, sessionmaker
from config import DATABASE
import math
import json
import pdb


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
        n_sig_up_genes = Column(Integer)
        n_sig_down_genes = Column(Integer)
        associations = relationship('Association')

    global Association
    class Association(Base):
        __tablename__ = 'association'
        id = Column(Integer, primary_key=True)
        signature_fk = Column(Integer, ForeignKey('signature.id'))
        gene_symbol = Column(String(25))
        fold_change = Column(Float)
        p_value = Column(Float)
        q_value = Column(Float)

        def get_row(self):
            s = get_or_create(session, Signature, id=self.signature_fk)[0]
            sig_id = s.sig_id
            pert_id = s.pert_id
            drug_name = s.drug_name
            pert_time = s.pert_time
            pert_time_unit = s.pert_time_unit
            pert_dose = s.pert_dose
            if self.fold_change > 0:
                specificity = 1./s.n_sig_up_genes
            else:
                specificity = 1./s.n_sig_down_genes

            return drug_name, \
                sig_id, \
                pert_id, \
                pert_time, \
                pert_time_unit, \
                pert_dose, \
                self.p_value, \
                self.q_value, \
                self.fold_change, \
                specificity


    global creedsSignature
    class creedsSignature(Base):
        __tablename__ = 'creeds_signature'
        id = Column(Integer, primary_key=True)
        creeds_id = Column(String(50), unique=True)
        drug_name = Column(String(100))
        geo_id = Column(String(50))
        drugbank_id = Column(String(50))
        pubchem_id = Column(String(50))
        n_sig_up_genes = Column(Integer)
        n_sig_down_genes = Column(Integer)
        associations = relationship('creedsAssociation')


    global creedsAssociation
    class creedsAssociation(Base):
        __tablename__ = 'creeds_association'
        id = Column(Integer, primary_key=True)
        signature_fk = Column(Integer, ForeignKey('creeds_signature.id'))
        gene_symbol = Column(String(25))
        p_value = Column(Float)
        q_value = Column(Float)
        fold_change = Column(Float)

        def get_row(self):
            cs = get_or_create(session, creedsSignature, id=self.signature_fk)[0]
            drug_name = cs.drug_name
            creeds_id = cs.creeds_id

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

            if self.fold_change > 0:
                specificity = 1./cs.n_sig_up_genes
            else:
                specificity = 1./cs.n_sig_down_genes

            return drug_name,\
                creeds_id,\
                geo_id,\
                drugbank_id,\
                pubchem_id,\
                self.p_value,\
                self.q_value,\
                self.fold_change,\
                specificity,\
                geo_url,\
                drugbank_url,\
                pubchem_url

    global CmapSignature
    class CmapSignature(Base):
        __tablename__ = 'cmap_signature'
        id = Column(Integer, primary_key=True)
        drug_name = Column(String(50))
        cell_name = Column(String(50))
        cell_info = Column(String(1000))
        pert_time = Column(Integer)
        pert_time_unit = Column(String(50))
        pert_dose = Column(Float)
        pert_dose_unit = Column(String(50))
        n_sig_up_genes = Column(Integer)
        n_sig_down_genes = Column(Integer)
        associations = relationship('CmapAssociation')

    global CmapAssociation
    class CmapAssociation(Base):
        __tablename__ = 'cmap_association'
        id = Column(Integer, primary_key=True)
        signature_fk = Column(Integer, ForeignKey('cmap_signature.id'))
        gene_symbol = Column(String(50))
        fold_change = Column(Float)
        p_value = Column(Float)
        q_value = Column(Float)

        def get_row(self):
            s = get_or_create(session, CmapSignature, id=self.signature_fk)[0]
            # sig_id = s.sig_id
            # pert_id = s.pert_id
            drug_name = s.drug_name
            cell_name = s.cell_name
            pert_time = s.pert_time
            pert_time_unit = s.pert_time_unit
            pert_dose = s.pert_dose
            if self.fold_change > 0:
                specificity = 1./s.n_sig_up_genes
            else:
                specificity = 1./s.n_sig_down_genes

            return drug_name, \
                cell_name, \
                pert_time, \
                pert_time_unit, \
                pert_dose, \
                self.p_value, \
                self.q_value, \
                self.fold_change, \
                specificity

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
    symbols = json.load(open('DGB/static/js/genes_list.json', 'r'))
    return symbol in symbols
    #     return True
    # else:
    #     return False


# ======================================= API =====================================================

def get_or_create_API(session, dataset,**kwargs):
    # init a instance if not exists
    # http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    if (dataset == 'CREEDS'):
        instance = session.query(creedsAssociation, creedsSignature).filter_by(**kwargs).join(creedsSignature, creedsAssociation.signature_fk==creedsSignature.id)
    else:
        instance = session.query(Association, Signature).filter_by(**kwargs).join(Signature, Association.signature_fk==Signature.id)

    if instance:
        return instance
    else:
        instance = Association(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def dataset_query(symbol, expression, dataset):
    init()
    association = get_or_create_API(session, dataset, gene_symbol=symbol)

    if (dataset == 'CREEDS'):
        assoc_table_name = 'creedsAssociation'
        sig_table_name = 'creedsSignature'
    else:
        assoc_table_name = 'Association'
        sig_table_name = 'Signature'

    res = []
    for entry in association:
        association = getattr(entry, assoc_table_name).__dict__
        if (expression == 'UP' and association['fold_change'] >= 0) or \
                (expression == 'DOWN' and association['fold_change'] <= 0):
            signature = getattr(entry, sig_table_name).__dict__
            dictret = dict(association)
            dictret.update(dict(signature))
            for e in ['_sa_instance_state', 'signature_fk', 'id', 'pert_dose_unit']: #temporary, must work on getting pert_dose_unit encoding working.
                dictret.pop(e, None)
            res.append(dictret)
    return res

# ======================================= Web App =====================================================

# This function will return a tuple; each entry of that tuple represents a row of the output table.
def get_lincs_rows(symbol, expression):

    init()
    association = get_or_create(session, Association, gene_symbol=symbol)
    total_count = association.count()
    associations = association[0:]
    rows = [None] * total_count

    for i in xrange(total_count):
        entry = associations[i]
        row = None
        if (expression == 'Up-Regulate' and entry.fold_change > 0) or \
                (expression == 'Down-Regulate' and entry.fold_change < 0):
            row = entry.get_row()
        rows[i] = row

    # Sort the lists in order of fold-change, and calculate decile scores for each association.
    rows = filter(None, rows)
    rows = sorted(rows, key=lambda tup: tup[7])
    length = len(rows)

    if length > 0:
        p_vals = [0] * length
        min_max_p_val = [min(p_vals), max(p_vals)]
        for i in xrange(length):
            p_vals[i] = rows[i][5]
        fold_changes = [0] * length
        for i in xrange(length):
            fold_changes[i] = rows[i][7]
    else:
        min_max_p_val = []

    result = (rows, min_max_p_val)
    return result


def get_creeds_rows(symbol, expression):
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
        if (expression == 'Up-Regulate' and entry.fold_change > 0) or \
                (expression == 'Down-Regulate' and entry.fold_change < 0):
            row = entry.get_row()
        creedsrows[i] = row

    # Sort the lists in order of fold-change, and calculate decile scores for each association.
    creedsrows = filter(None, creedsrows)
    # creedsrows = sorted(creedsrows, key=lambda tup: tup[5])
    length = len(creedsrows)

    if length > 0:
        p_vals = [0] * length
        min_max_p_val = [min(p_vals), max(p_vals)]
        for i in xrange(length):
            p_vals[i] = creedsrows[i][6]
        fold_changes = [0] * length
        for i in xrange(length):
            fold_changes[i] = creedsrows[i][5]
    else:
        min_max_p_val = []

    result = (creedsrows, min_max_p_val)
    return result

def get_cmap_rows(symbol, expression):

    init()
    association = get_or_create(session, CmapAssociation, gene_symbol=symbol)
    total_count = association.count()
    associations = association[0:]
    rows = [None] * total_count

    for i in xrange(total_count):
        entry = associations[i]
        row = None
        if entry.q_value < 0.05:
            if (expression == 'Up-Regulate' and entry.fold_change > 0) or \
                    (expression == 'Down-Regulate' and entry.fold_change < 0):
                row = entry.get_row()
        rows[i] = row

    # Sort the lists in order of fold-change, and calculate decile scores for each association.
    rows = filter(None, rows)
    rows = sorted(rows, key=lambda tup: tup[7])
    length = len(rows)

    if length > 0:
        p_vals = [0] * length
        min_max_p_val = [min(p_vals), max(p_vals)]
        for i in xrange(length):
            p_vals[i] = rows[i][5]
        fold_changes = [0] * length
        for i in xrange(length):
            fold_changes[i] = rows[i][7]
    else:
        min_max_p_val = []

    result = (rows, min_max_p_val)
    return result
