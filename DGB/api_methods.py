def find_l1000(symbol, expression):
    return { "Type": "L1000", "Analysis": symbol[::-1] }
    # return lincs_rows(symbol, expression)

def find_creeds(symbol, expression):
    return { "Type": "CREEDS", "Analysis": symbol[::-1] }
    # return creeds_rows(symbol, expression)

def find_both(symbol, expression):
    return { "Type": "BOTH!", "Analysis": symbol[::-1] }


# This function will return a tuple; each entry of that tuple represents a row of the output table.
# def lincs_rows(symbol, expression):
#
#     init()
#     association = get_or_create(session, Association, gene_symbol=symbol)
#     total_count = association.count()
#     associations = association[0:]
#     rows = [None] * total_count
#
#     for i in xrange(total_count):
#         entry = associations[i]
#         row = None
#         if (expression == 'Up' and entry.fold_change > 0) or \
#                 (expression == 'Down' and entry.fold_change < 0):
#             row = entry.get_row()
#         rows[i] = row
#
#     # Sort the lists in order of fold-change, and calculate decile scores for each association.
#     rows = filter(None, rows)
#     rows = sorted(rows, key=lambda tup: tup[7])
#     length = len(rows)
#
#     fold_changes = [0] * length
#     for i in xrange(length):
#         fold_changes[i] = rows[i][7]
#
#     deciles = decile_calculate(fold_changes)
#
#     # This will pass in a string to the output page, reminding the user of the option they chose (up vs down).
#     if expression == 'Up':
#         pattern = 'Up-Regulated'
#     else:
#         pattern = 'Down-Regulated'
#
#     result = (rows, deciles, pattern)
#     return result
