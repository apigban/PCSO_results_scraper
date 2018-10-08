#!/usr/bin/env python3.7

import requests
from lxml import html

uri = 'http://www.pcso.gov.ph/SearchLottoResult.aspx'

html_headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


def get_page():
    """
     retrieves raw html response using GET on uri and html_headers
     converts response string to an htmlElement object
    :return:
    """
    response = requests.get(uri, headers=html_headers)
    #print(response.content)
    page = html.fromstring(response.content)
    #print(page)
    return page


def extract_viewstate(raw_html):
    """
    locates @id="__VIEWSTATE" and returns the __VIEWSTATE value
    locates @id="__VIEWSTATEGENERATOR" and returns the __VIEWSTATEGENERATOR value
    len(viewstate) as of 20181008 is 5680
    len(viewstategenerator) as of 20181008 is 12
    :rtype: htmlElement object
    """
    viewstate = str(raw_html.xpath('//input[@id="__VIEWSTATE"]/@value'))
    viewstate_gen = str(raw_html.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value'))
    #print(viewstate)
    #print(type(viewstate))
    #print(len(viewstate))

    #print(viewstate_gen)
    #print(type(viewstate_gen))
    #print(len(viewstate_gen))

    return viewstate, viewstate_gen

def init_formfield():

    formfield = {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstate_gen,
        "ctl00$ctl00$cphContainer$cpContent$ddlStartMonth": "",
        "ctl00$ctl00$cphContainer$cpContent$ddlStartDate": "",
        "ctl00$ctl00$cphContainer$cpContent$ddlStartYear": "",
        "ctl00$ctl00$cphContainer$cpContent$ddlEndMonth": "",
        "ctl00$ctl00$cphContainer$cpContent$ddlEndDay": "",
        "ctl00$ctl00$cphContainer$cpContent$ddlEndYear": "",
        "ctl00$ctl00$cphContainer$cpContent$ddlSelectGame": "",
        "ctl00$ctl00$cphContainer$cpContent$btnSearch": ""


    }


raw_html = get_page()

viewstate, viewstate_gen = extract_viewstate(raw_html)


print(viewstate,viewstate_gen)