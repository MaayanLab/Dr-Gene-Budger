import json
from StringIO import StringIO
import pandas as pd
from pandas import ExcelWriter

from models import L1000Association, CreedsAssociation, CmapAssociation

def symbol_validate(symbol):
    symbols = json.load(open('DGB/static/js/genes_list.json', 'r'))
    return symbol in symbols

def filter_by_expression(query_results, association, expression):
    if (expression == 'Up-Regulate'):
        return query_results.having(association.fold_change >= 0).all()
    return query_results.having(association.fold_change < 0).all()


def make_excel_file(names, objects):
    '''Make excel file for the associations to a StringIO object.
    '''
    str_io = StringIO()
    writer = ExcelWriter(str_io, engine='xlsxwriter')
    for name, obj in zip(names, objects):
        df = pd.DataFrame([assc.to_table_row() for assc in obj])
        df.to_excel(writer, name, index=True)
    writer.save()
    str_io.seek(0)
    return str_io


# Model Methods
def get_or_create(session, model, **kwargs):
    # init a instance if not exists
    # http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    instance = session.query(model).filter_by(**kwargs).order_by(model.p_value)
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def separate_by_expression(model_query):
    results = { "up": [], "down": []}
    for query_item in model_query:
        if (query_item.fold_change >= 0):
            results["up"].append(query_item.to_json())
        else:
            results["down"].append(query_item.to_json())
    return results


def get_rows(session, symbol):
    return {
        "l1000_query": get_or_create(session, L1000Association, gene_symbol=symbol),
        "creeds_query": get_or_create(session, CreedsAssociation, gene_symbol=symbol),
        "cmap_query": get_or_create(session, CmapAssociation, gene_symbol=symbol)
    }

def mobile_get_rows(session, symbol):
    l1000 = separate_by_expression(get_or_create(session, L1000Association, gene_symbol=symbol))
    creeds = separate_by_expression(get_or_create(session, CreedsAssociation, gene_symbol=symbol))
    cmap = separate_by_expression(get_or_create(session, CmapAssociation, gene_symbol=symbol))

    return {
        "l1000_query": l1000,
        "creeds_query": creeds,
        "cmap_query": cmap
    }
