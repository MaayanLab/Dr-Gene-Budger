def find_l1000(symbol, expression):
    return { "Type": "L1000", "Analysis": symbol[::-1] }
    # return lincs_rows(symbol, expression)

def find_creeds(symbol, expression):
    return { "Type": "CREEDS", "Analysis": symbol[::-1] }
    # return creeds_rows(symbol, expression)

def find_both(symbol, expression):
    return { "Type": "BOTH!", "Analysis": symbol[::-1] }
