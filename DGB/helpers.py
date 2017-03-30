import json

def symbol_validate(symbol):
    symbols = json.load(open('DGB/static/js/genes_list.json', 'r'))
    return symbol in symbols
