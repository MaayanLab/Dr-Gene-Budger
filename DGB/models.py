from app import db

class Signature(db.Model):
    __tablename__ = 'signature'
    id = db.Column(db.Integer, primary_key=True)
    sig_id = db.Column(db.String(50))
    pert_id = db.Column(db.String(20))
    drug_name = db.Column(db.String(50))
    pert_time = db.Column(db.Integer)
    pert_time_unit = db.Column(db.String(6))
    pert_dose = db.Column(db.Float)
    pert_dose_unit = db.Column(db.String(6))
    n_sig_up_genes = db.Column(db.Integer)
    n_sig_down_genes = db.Column(db.Integer)
    associations = db.relationship('Association', backref="association")

    def __init__(self, id, sig_id, pert_id, drug_name,
               pert_time, pert_time_unit, pert_dose,
               pert_dose_unit, n_sig_up_genes, n_sig_down_genes):
        self.id = id
        self.sig_id = sig_id
        self.pert_id = pert_id
        self.pert_time = pert_time
        self.pert_time_unit = pert_time_unit
        self.pert_dose = pert_dose
        self.pert_dose_unit = pert_dose_unit
        self.n_sig_up_genes = n_sig_up_genes
        self.n_sig_down_genes = n_sig_down_genes
        self.associations = associations

class Association(db.Model):
    __tablename__ = 'association'
    id = db.Column(db.Integer, primary_key=True)
    signature_fk = db.Column(db.Integer, db.ForeignKey('signature.id'))
    gene_symbol = db.Column(db.String(25))
    fold_change = db.Column(db.Float)
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    signature = db.relationship("Signature", backref="signature")

    def __init__(self, id, signature_fk, gene_symbol,
                 fold_change, p_value, q_value):
        self.id = id
        self.signature_fk = signature_fk
        self.gene_symbol = gene_symbol
        self.fold_change = fold_change
        self.p_value = p_value
        self.q_value = q_value
        self.signature = signature

class creedsSignature(db.Model):
    __tablename__ = 'creeds_signature'
    id = db.Column(db.Integer, primary_key=True)
    creeds_id = db.Column(db.String(50), unique=True)
    drug_name = db.Column(db.String(100))
    geo_id = db.Column(db.String(50))
    drugbank_id = db.Column(db.String(50))
    pubchem_id = db.Column(db.String(50))
    n_sig_up_genes = db.Column(db.Integer)
    n_sig_down_genes = db.Column(db.Integer)
    associations = db.relationship('creedsAssociation', backref="creedsAssociation")

    def __init__(self, id, creeds_id, drug_name, geo_id,
                 drugbank_id, pubchem_id, n_sig_up_genes,
                 n_sig_down_genes, associations):
        self.id = id
        self.creeds_id = creeds_id
        self.drug_name = drug_name
        self.geo_id = geo_id
        self.drugbank_id = drugbank_id
        self.pubchem_id = pubchem_id
        self.n_sig_up_genes = n_sig_up_genes
        self.n_sig_down_genes = n_sig_down_genes
        self.associations = associations

class creedsAssociation(db.Model):
    __tablename__ = 'creeds_association'
    id = db.Column(db.Integer, primary_key=True)
    signature_fk = db.Column(db.Integer, db.ForeignKey('creeds_signature.id'))
    gene_symbol = db.Column(db.String(25))
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    fold_change = db.Column(db.Float)
    signature = db.relationship("creedsSignature", backref="creedsSignature")

    def __init__(self, id, signature_fk, gene_symbol,
                 fold_change, p_value, q_value):
        self.id = id
        self.signature_fk = signature_fk
        self.gene_symbol = gene_symbol
        self.p_value = p_value
        self.q_value = q_value
        self.fold_change = fold_change
        self.signature = signature

class CmapSignature(db.Model):
    __tablename__ = 'cmap_signature'
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(50))
    cell_name = db.Column(db.String(50))
    cell_info = db.Column(db.String(1000))
    pert_time = db.Column(db.Integer)
    pert_time_unit = db.Column(db.String(50))
    pert_dose = db.Column(db.Float)
    pert_dose_unit = db.Column(db.String(50))
    n_sig_up_genes = db.Column(db.Integer)
    n_sig_down_genes = db.Column(db.Integer)
    associations = db.relationship('CmapAssociation', backref="cmapAssociation")

    def __init__(self, id, drug_name, cell_name, cell_info,
                 pert_time, pert_time_unit, pert_dose,
                 pert_dose_unit, n_sig_up_genes,
                 n_sig_down_genes, associations):
        self.id = id
        self.drug_name = drug_name
        self.cell_name = cell_name
        self.cell_info = cell_info
        self.pert_time = pert_time
        self.pert_time_unit = pert_time_unit
        self.pert_dose = pert_dose
        self.pert_dose_unit = pert_dose_unit
        self.n_sig_up_genes = n_sig_up_genes
        self.n_sig_down_genes = n_sig_down_genes
        self.associations = associations

class CmapAssociation(db.Model):
    __tablename__ = 'cmap_association'
    id = db.Column(db.Integer, primary_key=True)
    signature_fk = db.Column(db.Integer, db.ForeignKey('cmap_signature.id'))
    gene_symbol = db.Column(db.String(50))
    fold_change = db.Column(db.Float)
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    signature = db.relationship("CmapSignature", backref="cmapSignature")

    def __init__(self, id, signature_fk, gene_symbol,
                 fold_change, p_value, q_value):
        self.id = id
        self.signature_fk = signature_fk
        self.gene_symbol = gene_symbol
        self.fold_change = fold_change
        self.p_value = p_value
        self.q_value = q_value
        self.signature = signature

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

def get_l1000_rows(session, symbol, expression):
    if (expression == 'Up-Regulate'):
        associations = get_or_create(session, Association, gene_symbol=symbol).having(Association.fold_change >= 0).all()
    else:
        associations = get_or_create(session, Association, gene_symbol=symbol).having(Association.fold_change < 0).all()
    return associations
    # rows = [None] * total_count

    # for i in xrange(total_count):
    #     entry = associations[i]
    #     row = None
    #     if (expression == 'Up-Regulate' and entry.fold_change > 0) or \
    #             (expression == 'Down-Regulate' and entry.fold_change < 0):
    #         row = entry.get_row()
    #     rows[i] = row
    #
    # # Sort the lists in order of fold-change, and calculate decile scores for each association.
    # rows = filter(None, rows)
    # rows = sorted(rows, key=lambda tup: tup[7])
    # length = len(rows)
    #
    # if length > 0:
    #     p_vals = [0] * length
    #     min_max_p_val = [min(p_vals), max(p_vals)]
    #     for i in xrange(length):
    #         p_vals[i] = rows[i][5]
    #     fold_changes = [0] * length
    #     for i in xrange(length):
    #         fold_changes[i] = rows[i][7]
    # else:
    #     min_max_p_val = []
    #
    # result = (rows, min_max_p_val)
    # return result


def get_creeds_rows(session, symbol, expression):
    if (expression == 'Up-Regulate'):
        creedsassociations = get_or_create(session, creedsAssociation, gene_symbol=symbol).having(creedsAssociation.fold_change >= 0).all()
    else:
        creedsassociations = get_or_create(session, creedsAssociation, gene_symbol=symbol).having(creedsAssociation.fold_change < 0).all()
    return creedsassociations
    # total_count = creedsassociation.count()
    # creedsrows = [None] * total_count
    #
    # for i in xrange(total_count):
    #     entry = creedsassociations[i]
    #     # This if statement ensures that we only extract the associations with desired expression patterns.
    #     row = None
    #     if (expression == 'Up-Regulate' and entry.fold_change > 0) or \
    #             (expression == 'Down-Regulate' and entry.fold_change < 0):
    #         row = entry.get_row()
    #     creedsrows[i] = row
    #
    # # Sort the lists in order of fold-change, and calculate decile scores for each association.
    # creedsrows = filter(None, creedsrows)
    # # creedsrows = sorted(creedsrows, key=lambda tup: tup[5])
    # length = len(creedsrows)
    #
    # if length > 0:
    #     p_vals = [0] * length
    #     min_max_p_val = [min(p_vals), max(p_vals)]
    #     for i in xrange(length):
    #         p_vals[i] = creedsrows[i][6]
    #     fold_changes = [0] * length
    #     for i in xrange(length):
    #         fold_changes[i] = creedsrows[i][5]
    # else:
    #     min_max_p_val = []
    #
    # result = (creedsrows, min_max_p_val)
    # return result

def get_cmap_rows(session, symbol, expression):
    if (expression == 'Up-Regulate'):
        associations = get_or_create(session, CmapAssociation, gene_symbol=symbol).having(CmapAssociation.fold_change >= 0).all()
    else:
        associations = get_or_create(session, CmapAssociation, gene_symbol=symbol).having(CmapAssociation.fold_change < 0).all()
    return associations
    # rows = [None] * total_count
    #
    # for i in xrange(total_count):
    #     entry = associations[i]
    #     row = None
    #     if entry.q_value < 0.05:
    #         if (expression == 'Up-Regulate' and entry.fold_change > 0) or \
    #                 (expression == 'Down-Regulate' and entry.fold_change < 0):
    #             row = entry.get_row()
    #     rows[i] = row
    #
    # # Sort the lists in order of fold-change, and calculate decile scores for each association.
    # rows = filter(None, rows)
    # rows = sorted(rows, key=lambda tup: tup[7])
    # length = len(rows)
    #
    # if length > 0:
    #     p_vals = [0] * length
    #     min_max_p_val = [min(p_vals), max(p_vals)]
    #     for i in xrange(length):
    #         p_vals[i] = rows[i][5]
    #     fold_changes = [0] * length
    #     for i in xrange(length):
    #         fold_changes[i] = rows[i][7]
    # else:
    #     min_max_p_val = []
    #
    # result = (rows, min_max_p_val)
    # return result
