import requests
from datetime import date
from .filter import tmc_filter


def get_tmc(tmc_form):

    query_date = tmc_form.cleaned_data['query_date']
    year_str = str(query_date.year)
    month = query_date.month
    month_str = '0' + str(month) if month < 10 else str(month)
    one_month_ago = date(query_date.year, query_date.month - 1, query_date.day)
    year_one_month_ago_str = str(one_month_ago.year)
    month_one_month_ago = one_month_ago.month
    month_one_month_ago_str = '0' + str(month_one_month_ago) if month_one_month_ago < 10 else str(month_one_month_ago)

    apikey = '9c84db4d447c80c74961a72245371245cb7ac15f'
    date_range = year_one_month_ago_str + '/' + month_one_month_ago_str + '/' + year_str + '/' + month_str
    pathGet = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/periodo/' + date_range +'?apikey=' + apikey + '&formato=JSON'

    try:
        r = requests.get(pathGet)
    except:
        print("No fue posible obtener TMC")
    if r.status_code != 200:
        print("No fue posible obtener TMC")

    body_response_filtered = tmc_filter(r.json()['TMCs'],
                                        tmc_form.cleaned_data['credit_amount'],
                                        tmc_form.cleaned_data['time_to_maturity'],
                                        tmc_form.cleaned_data['query_date'],
                                        tmc_form.cleaned_data['credit_type'])
    return body_response_filtered
    # html = "<html><body>It is now %s.</body></html>" % r.json()['TMCs']
    # html = "<html><body>It is now %s.</body></html>" % body_response_filtered_by_amount_in_uf
    # return HttpResponse(html)
