from datetime import date
import re


# assumption 1: the member 'Subtitulo' only says 'unidades de fomento' if is the UF case
# assumption 2: the lower bound comes after the string 'uperiores al equivalente de '
# assumption 3: the upper bound comes after the string 'nferiores o iguales al equivalente de '
# assumption 4: if no 'Hasta' is provided it will be assumed that the tmc is valid for one month
# assumption 5: the credit can be only one of the followings: 'No reajustable', 'Reajustable' or 'Moneda extranjera'


def tmc_filter(tmcs, credit_amount, time_to_maturity, query_date, credit_type):
    tmcs_without_none = filter_non_null(tmcs)

    tmcs_filtered_by_type = filter_by_type(tmcs_without_none, credit_type)

    tmcs_filtered_by_date = filter_by_date(tmcs_filtered_by_type, query_date)

    tmcs_filtered_by_maturity= filter_by_maturity(tmcs_filtered_by_date, time_to_maturity, credit_type)

    return filter_by_amount(tmcs_filtered_by_maturity, credit_amount)

def filter_non_null(tmcs):
    # remove non UF
    tmcs_filtered = []
    for tmc in tmcs:
        if tmc['Titulo'] != None:
            tmcs_filtered.append(tmc)
    return tmcs_filtered

def filter_by_type(tmcs, credit_type):
    tmcs_of_type = []
    for tmc in tmcs:
        if tmc['Titulo'].find(credit_type) != -1:
            tmcs_of_type.append(tmc)
    return tmcs_of_type


def filter_by_amount(tmcs, credit_amount):
    # get range of UF
    tmcs_in_range = []
    for tmc in tmcs:
        # get upper bound
        matched_upper_bound = re.search(r'(?<=nferiores o iguales al equivalente de )[0-9|/.]+', tmc['SubTitulo'])
        upper_bound_str = matched_upper_bound.group(0).replace(".", "") if matched_upper_bound != None else '100000000000'  # I HATE this number but it looks like Python doesn't have std::numeric_limits<int>::max()
        upper_bound = int(upper_bound_str)
        # get lower bound
        matched_lower_bound = re.search(r'(?<=uperiores al equivalente de )[0-9|/.]+', tmc['SubTitulo'])
        lower_bound_str = matched_lower_bound.group(0).replace(".", "") if matched_lower_bound != None else '0'
        lower_bound = int(lower_bound_str)
        # compare
        if lower_bound < credit_amount <= upper_bound:
            tmcs_in_range.append(tmc)
    return tmcs_in_range


def filter_by_date(tmcs, query_date):
    filtered_tmcs = []
    for tmc in tmcs:
        beginning_date = to_date(tmc['Fecha'])
        ending_date = to_date(tmc['Hasta'])
        if beginning_date <= query_date <= ending_date:
            filtered_tmcs.append(tmc)
    return filtered_tmcs


def filter_by_maturity(tmcs, time_to_maturity, credit_type):
    filtered_tmcs = []
    if credit_type == 'Operaciones expresadas en moneda extranjera':
        return tmcs

    # no reajustable, titulo: '90 días o más', 'de menos de 90 días'
    elif credit_type == 'Operaciones no reajustables':
        for tmc in tmcs:
            if (tmc['Titulo'].find('90 días o más') != -1 and time_to_maturity >= 90) or (tmc['Titulo'].find('de menos de 90 días') != -1 and time_to_maturity < 90):
                filtered_tmcs.append(tmc)

    # reajustable,sub 'De un año o más', 'Menores a un año'
    else:
        for tmc in tmcs:
            if (tmc['SubTitulo'].find('De un año o más') != -1 and time_to_maturity >= 365) or (tmc['SubTitulo'].find('Menores a un año') != -1 and time_to_maturity < 365):
                filtered_tmcs.append(tmc)

    return filtered_tmcs


def to_date(date_str):
    if date_str == None:
        return date(date.today().year, date.today().month + 1, date.today().day)
    date_array = date_str.split('-')
    return date(int(date_array[0]), int(date_array[1]), int(date_array[2]))
