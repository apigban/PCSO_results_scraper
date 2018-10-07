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
    print(response.content)
    page = html.fromstring(response.content)
    print(page)
    return page


def extract_viewstate(raw_html):
    """
    locates @id="__VIEWSTATE" and returns the __VIEWSTATE value
    len(viewstate) as of 20181008 is 5680
    :rtype: htmlElement object
    """
    viewstate = str(raw_html.xpath('//input[@id="__VIEWSTATE"]/@value'))
    print(viewstate)
    print(type(viewstate))
    print(len(viewstate))
    return viewstate


raw_html = get_page()

extract_viewstate(raw_html)
