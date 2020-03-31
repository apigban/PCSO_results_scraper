import os

from tests.aux_methods import find_files
from scraper_app import Extraction, Log


def test_sqlite_db_exists():
    """
    Tests if sqlite database exists on project path    
    """
    assert find_files(":PCSO.sqlite", "/home/pythonsvc/PCSO_results_scraper/scraper_app") == True 

def test_sqlite_db_exists():
    """
    Tests if sqlite database exists on project path    
    """
    assert find_files(":PCSO.sqlite", "/home/pythonsvc/PCSO_results_scraper/scraper_app") == True 