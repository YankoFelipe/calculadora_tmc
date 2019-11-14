from datetime import date
import re

# assumption 1: the member 'Subtitulo' only says 'unidades de fomento' if is the UF case
# assumption 2: the lower bound comes after the string 'uperiores al equivalente de '
# assumption 3: the upper bound comes after the string 'nferiores o iguales al equivalente de '
# assumption 4: if no 'Hasta' is provided it will be assumed that the tmc is valid for one month
# assumption 5: the credit can be only one of the followings: 'No reajustable', 'Reajustable' or 'Moneda extranjera'

def tmc_filter(tmcs, credit_amount, time_to_maturity, query_date, credit_type):
    tmcs_filtered_by_amount_in_uf = filter_by_uf(tmcs, credit_amount)

    tmcs_filtered_by_date = filter_by_date(tmcs_filtered_by_amount_in_uf, query_date)

    ret = tmcs_filtered_by_date
    return ret


def filter_by_uf(tmcs, credit_amount):
    # remove non UF
    tmcs_in_uf = []
    for tmc in tmcs:
        if tmc['SubTitulo'].find('unidades de fomento') != -1:
            tmcs_in_uf.append(tmc)
    # get range of UF
    tmcs_in_range = []
    for tmc in tmcs_in_uf:
        # get upper bound
        matched_upper_bound = re.search(r'(?<=nferiores o iguales al equivalente de )[0-9|/.]+', tmc['SubTitulo'])
        upper_bound_str = matched_upper_bound.group(0).replace(".", "") if matched_upper_bound != None else '100000000000' # I HATE this number but it looks like Python doesn't have std::numeric_limits<int>::max()
        upper_bound = int(upper_bound_str)
        # get lower bound
        matched_lower_bound = re.search(r'(?<=uperiores al equivalente de )[0-9|/.]+', tmc['SubTitulo'])
        lower_bound_str = matched_lower_bound.group(0).replace(".", "") if matched_lower_bound != None else '0'
        lower_bound = int(lower_bound_str)
        # compare
        if lower_bound < credit_amount <= upper_bound:
            tmcs_in_range.append(tmc)
    return tmcs_in_range

def filter_by_date(tmcs, credit_date):
    filtered_tmcs = []
    for tmc in tmcs:
        beginning_date = to_date(tmc['Fecha'])
        ending_date = to_date(tmc['Hasta'])
        if beginning_date <= credit_date <= ending_date:
            filtered_tmcs.append(tmc)
    return tmcs

def to_date(date_str):
    if date_str == None:
        return date(date.today().year, date.today().month + 1, date.today().day)
    date_array = date_str.split('-')
    return date(int(date_array[0]), int(date_array[1]), int(date_array[2]))