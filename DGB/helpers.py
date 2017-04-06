import json
from models import L1000Association, CreedsAssociation, CmapAssociation

def symbol_validate(symbol):
    symbols = json.load(open('DGB/static/js/genes_list.json', 'r'))
    return symbol in symbols

def filter_by_expression(query_results, association, expression):
    if (expression == 'Up-Regulate'):
        return query_results.having(association.fold_change >= 0).all()
    return query_results.having(association.fold_change < 0).all()

# Model Methods
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

def get_rows(session, symbol):
    return {
        "l1000_query": get_or_create(session, L1000Association, gene_symbol=symbol),
        "creeds_query": get_or_create(session, CreedsAssociation, gene_symbol=symbol),
        "cmap_query": get_or_create(session, CmapAssociation, gene_symbol=symbol)
    }
