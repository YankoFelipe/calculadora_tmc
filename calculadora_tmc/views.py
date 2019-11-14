import requests
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from .filter import tmc_filter
from .forms import TmcForm
from .api import get_tmc

def data(request):
    year = 2019
    month = '09'
    apikey = '9c84db4d447c80c74961a72245371245cb7ac15f'
    pathGet = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/' + str(year) + '/' + month +'?apikey=' + apikey + '&formato=JSON'
    r = requests.get(pathGet)
    # if (r.status_code != 200)
    body_response_filtered_by_amount_in_uf = tmc_filter(r.json()['TMCs'], 2000, date.today(), False, False)
    # html = "<html><body>It is now %s.</body></html>" % r.json()['TMCs']
    html = "<html><body>It is now %s.</body></html>" % body_response_filtered_by_amount_in_uf
    return HttpResponse(html)


def tmcform(request):
    # creating a new form
    form = TmcForm(request.GET)
    tmc = ''

    if form.is_valid():
        tmc = get_tmc(form)

    # returning form
    return render(request, 'tmcform.html', {'form': form, 'tmc': tmc})
