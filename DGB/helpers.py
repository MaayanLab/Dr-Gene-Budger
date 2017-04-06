import json

def symbol_validate(symbol):
    symbols = json.load(open('DGB/static/js/genes_list.json', 'r'))
    return symbol in symbols

def filter_by_expression(query_results, association, expression):
    if (expression == 'Up-Regulate'):
        return query_results.having(association.fold_change >= 0).all()
    return query_results.having(association.fold_change < 0).all()
