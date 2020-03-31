import os

def find_files(file_name, search_path):
    result = None
    for root, dir, files in os.walk(search_path):
        if file_name in files:
            result = True
    return result

if __name__ == '__main__':
    print('Module Executed Independently.')
    file_name = ":PCSO.sqlite"
    search_path = "/home/pythonsvc/PCSO_results_scraper/scraper_app"
    print(find_files(file_name,search_path))