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

class Association(db.Model):
    __tablename__ = 'association'
    id = db.Column(db.Integer, primary_key=True)
    signature_fk = db.Column(db.Integer, db.ForeignKey('signature.id'))
    gene_symbol = db.Column(db.String(25))
    fold_change = db.Column(db.Float)
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    signature = db.relationship("Signature", backref="signature")

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

class creedsAssociation(db.Model):
    __tablename__ = 'creeds_association'
    id = db.Column(db.Integer, primary_key=True)
    signature_fk = db.Column(db.Integer, db.ForeignKey('creeds_signature.id'))
    gene_symbol = db.Column(db.String(25))
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    fold_change = db.Column(db.Float)
    signature = db.relationship("creedsSignature", backref="creedsSignature")

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

class CmapAssociation(db.Model):
    __tablename__ = 'cmap_association'
    id = db.Column(db.Integer, primary_key=True)
    signature_fk = db.Column(db.Integer, db.ForeignKey('cmap_signature.id'))
    gene_symbol = db.Column(db.String(50))
    fold_change = db.Column(db.Float)
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    signature = db.relationship("CmapSignature", backref="cmapSignature")

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
