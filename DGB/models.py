from app import db
from mixin import OutputMixin

class L1000Signature(OutputMixin, db.Model):
    __tablename__ = 'l1000_signatures'
    id = db.Column(db.Integer, primary_key=True)
    sig_id = db.Column(db.String(50))
    pert_id = db.Column(db.String(20))
    pubchem_cid = db.Column(db.String(50))
    drugbank_id = db.Column(db.String(50))
    drug_name = db.Column(db.String(50))
    pert_time = db.Column(db.Integer)
    pert_time_unit = db.Column(db.String(6))
    pert_dose = db.Column(db.Float)
    pert_dose_unit = db.Column(db.String(6))
    n_sig_up_genes = db.Column(db.Integer)
    n_sig_down_genes = db.Column(db.Integer)

class L1000Association(OutputMixin, db.Model):
    __tablename__ = 'l1000_associations'
    RELATIONSHIPS_TO_DICT = True

    id = db.Column(db.Integer, primary_key=True)
    l1000_signature_id = db.Column('l1000_signature_id', db.Integer, db.ForeignKey('l1000_signatures.id'))
    gene_symbol = db.Column(db.String(25))
    fold_change = db.Column(db.Float)
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    signature = db.relationship("L1000Signature", backref=db.backref("l1000_associations", lazy="dynamic"))

class CreedsSignature(OutputMixin, db.Model):
    __tablename__ = 'creeds_signatures'
    id = db.Column(db.Integer, primary_key=True)
    creeds_id = db.Column(db.String(50), unique=True)
    drug_name = db.Column(db.String(100))
    geo_id = db.Column(db.String(50))
    drugbank_id = db.Column(db.String(50))
    pubchem_id = db.Column(db.String(50))
    n_sig_up_genes = db.Column(db.Integer)
    n_sig_down_genes = db.Column(db.Integer)

class CreedsAssociation(OutputMixin, db.Model):
    __tablename__ = 'creeds_associations'
    RELATIONSHIPS_TO_DICT = True

    id = db.Column(db.Integer, primary_key=True)
    creeds_signature_id = db.Column('creeds_signature_id', db.Integer, db.ForeignKey('creeds_signatures.id'))
    gene_symbol = db.Column(db.String(25))
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    fold_change = db.Column(db.Float)
    signature = db.relationship("CreedsSignature", backref=db.backref("creeds_associations", lazy="dynamic"))

class CmapSignature(OutputMixin, db.Model):
    __tablename__ = 'cmap_signatures'
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

class CmapAssociation(OutputMixin, db.Model):
    __tablename__ = 'cmap_associations'
    RELATIONSHIPS_TO_DICT = True

    id = db.Column(db.Integer, primary_key=True)
    cmap_signature_id = db.Column('cmap_signature_id', db.Integer, db.ForeignKey('cmap_signatures.id'))
    gene_symbol = db.Column(db.String(50))
    fold_change = db.Column(db.Float)
    p_value = db.Column(db.Float)
    q_value = db.Column(db.Float)
    signature = db.relationship("CmapSignature", backref=db.backref("cmap_associations", lazy="dynamic"))
