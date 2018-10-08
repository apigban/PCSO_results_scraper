#!/usr/bin/env python3.7

import requests
from lxml import html

def get_page():
    """
     retrieves raw html response using GET on uri and html_headers
     converts response string to an htmlElement object
    :return:
    """
    response = web_session.get(uri, headers=html_headers)
    #print(response.content)
    page = html.fromstring(response.content)
    #print(type(response))

    return page, response


def extract_state(raw_html):
    """
    locates @id="__VIEWSTATE" and returns the __VIEWSTATE value
    locates @id="__VIEWSTATEGENERATOR" and returns the __VIEWSTATEGENERATOR value
    locates @id="__EVENT..." and returns the __EVENT... value
    :rtype: htmlElement object
    """
    viewstate = str(raw_html.xpath('//input[@id="__VIEWSTATE"]/@value'))
    viewstate_gen = str(raw_html.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value'))
    event_validation = str(raw_html.xpath('//input[@id="__EVENTVALIDATION"]/@value'))
    event_target = str(raw_html.xpath('//input[@id="__EVENTTARGET"]/@value'))
    event_argument = str(raw_html.xpath('//input[@id="__EVENTARGUMENT"]/@value'))

    #print(event_validation, event_target, event_argument)
    #print(type(viewstate))
    #print(len(event_validation), len(event_target), len(event_argument))

    #print(viewstate_gen)
    #print(type(viewstate_gen))
    #print(len(viewstate_gen))

    return viewstate, viewstate_gen, event_validation, event_target, event_argument

def post_formfield(response):

    formfield = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstate_gen,
        '__EVENTTARGET': event_target,
        '__EVENTARGUMENT': event_argument,
        '__EVENTVALIDATION': event_validation,
        'ctl00$ctl00$cphContainer$cpContent$ddlStartMonth': 'January',
        'ctl00$ctl00$cphContainer$cpContent$ddlStartDate': '1',
        'ctl00$ctl00$cphContainer$cpContent$ddlStartYear': '2008',
        'ctl00$ctl00$cphContainer$cpContent$ddlEndMonth': 'October',
        'ctl00$ctl00$cphContainer$cpContent$ddlEndDay': '8',
        'ctl00$ctl00$cphContainer$cpContent$ddlEndYear': '2018',
        'ctl00$ctl00$cphContainer$cpContent$ddlSelectGame': '0',        #value=0 is ALL GAMES
        'ctl00$ctl00$cphContainer$cpContent$btnSearch': ''
    }

    web_session.post(uri, data=formfield)

uri = 'http://www.pcso.gov.ph/SearchLottoResult.aspx'

html_headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

web_session = requests.Session()

raw_html, response = get_page()

viewstate, viewstate_gen, event_validation, event_target, event_argument = extract_state(raw_html)


#print(viewstate,viewstate_gen)