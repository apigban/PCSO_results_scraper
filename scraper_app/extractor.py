#!/usr/bin/env python3.7

import requests, calendar
from lxml import html
from Extraction import db_writer_sqlite
from Log import log


scraper_logger = log.get_logger(__name__)

def get_page():
    """
     retrieves raw html response using GET on uri and html_headers
     converts response string to an htmlElement object
    :return:
    """
    pcso_response = web_session.get(uri, headers=html_headers)
    pcso_page = html.fromstring(pcso_response.content)

    return pcso_page, pcso_response


def extract_state(raw_html):
    """
    locates @id="__VIEWSTATE" and returns the __VIEWSTATE value
    locates @id="__VIEWSTATEGENERATOR" and returns the __VIEWSTATEGENERATOR value
    locates @id="__EVENT..." and returns the __EVENT... value

    ISSUE: Using xpath search, __VIEWSTATE, __VIEWSTATEGENERATOR and __EVENTVALIDATION results
    in a string that is enclosed with ['string']. Method below is to strip the full string using
    slice[2:-2] to strip the first and last 2 elements of the string. LOOK FOR A BETTER METHOD...

    :rtype: htmlElement object
    """
    viewstate = str(raw_html.xpath('//input[@id="__VIEWSTATE"]/@value'))
    viewstate = viewstate[2:-2]
    viewstate_gen = str(raw_html.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value'))
    viewstate_gen = viewstate_gen[2:-2]
    event_validation = str(raw_html.xpath('//input[@id="__EVENTVALIDATION"]/@value'))
    event_validation = event_validation[2:-2]
    event_target = str(raw_html.xpath('//input[@id="__EVENTTARGET"]/@value'))
    event_argument = str(raw_html.xpath('//input[@id="__EVENTARGUMENT"]/@value'))

    return viewstate, viewstate_gen, event_validation, event_target, event_argument


def post_formfield(response):
    """
    creates formfield dictionary containing form data to be sent by POST method
    POSTs the data to the asp.net form
    :rtype: requests.Response object
    """
    start_date, end_date = db_writer_sqlite.db_update_from_last_entry()

    formfield = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstate_gen,
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__EVENTVALIDATION': event_validation,
        'ctl00$ctl00$cphContainer$cpContent$ddlStartMonth': calendar.month_name[start_date.month],
        'ctl00$ctl00$cphContainer$cpContent$ddlStartDate': start_date.day,
        'ctl00$ctl00$cphContainer$cpContent$ddlStartYear': start_date.year,
        'ctl00$ctl00$cphContainer$cpContent$ddlEndMonth': calendar.month_name[end_date.month],
        'ctl00$ctl00$cphContainer$cpContent$ddlEndDay': end_date.day,
        'ctl00$ctl00$cphContainer$cpContent$ddlEndYear': end_date.year,
        'ctl00$ctl00$cphContainer$cpContent$ddlSelectGame': '0',  # value=0 is ALL GAMES
        'ctl00$ctl00$cphContainer$cpContent$btnSearch': 'Search+Lotto'
    }

    post_html = web_session.post(uri, headers=html_headers, data=formfield)
    return post_html


def file_write(line):
    """
    appends line of type str to lotto.full file
    list is first converted to a string
    line is stripped of 1st and last characters "[" and "]"
    """
    with open('lotto.full', 'a') as write_file:
        write_file.write(str(line)[1:-1])
        write_file.write('\n')

    scraper_logger.info(f'finished writing to {write_file}')

if __name__ == "__main__":

    uri = 'http://www.pcso.gov.ph/SearchLottoResult.aspx'

    html_headers = {
        'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.pcso.gov.ph/SearchLottoResult.aspx'
    }

    web_session = requests.Session()

    raw_html, response = get_page()

    viewstate, viewstate_gen, event_validation, event_target, event_argument = extract_state(raw_html)
    #print(response.content)
    full_html = html.fromstring(post_formfield(response).content)

    # print(full_html.text_content())
    rows = full_html.xpath('//table[@id="cphContainer_cpContent_GridView1"]')[0].findall('tr')

    parsed_table = list()
    # print(parsed_table)
    for row in reversed(rows[1:]):
        parsed_table.append([c.text for c in row.getchildren()])

    # SQLite
    # CREATE  DB and DUMP rows
    db_writer_sqlite.db_commit(parsed_table)

    # Postgresql
    # CREATE DB and DUMP rows
    #db_writer_postgres.db_commit(parsed_table)

    # RETURN LATEST ENTRY
    # db_writer_postgres.db_check_last_update()

    # ONLY USE FOR writing to file
    # for row in parsed_table:
    #    file_write(row)
    #    print(row)
