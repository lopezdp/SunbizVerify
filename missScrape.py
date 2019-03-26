#!/usr/bin/env python3

import mechanize
import argparse
import re
import json
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time

def searchState(searchQuery):
    # Start selenium...
    driver = webdriver.Chrome();
    driver.get("https://corp.sos.ms.gov/corp/portal/c/page/corpBusinessIdSearch/portal.aspx?#clear=1")
    
    # Get text input element
    elem = driver.find_element_by_id("businessNameTextBox")
    elem.send_keys(searchQuery)
    submit = driver.find_element_by_id("businessNameSearchButton")
    submit.click()

    # Wait for results to load
    try:
        elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "k-grid")))
    except TimeoutException:
        print("businessSearchResultsDiv not found!")
    
    # Insert error handling here!
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')  
    tags = soup.find_all("tr", {"role" : "row"})
    activeBusinesses = [] 

    for index, tag in enumerate(tags):
        if(tag.find("td", string="Good Standing")):
            # First gridcell is the name of the company...
            activeBusinesses.append(tag.find("td", {"role" : "gridcell"}).string)
            #print(tag.find("td", {"role" : "gridcell"}).string, "\n")
    
    return activeBusinesses

def main(args):
    results = searchState(args.searchQuery)

    # Output results
    if(args.json):
        print(json.dumps({'data' : results, 'state' : 'Mississippi'}, sort_keys=True,
                         indent=4, separators=(',', ': ')))
    else:
        print(f'Found {len(results)} active businesses while searching for {args.searchQuery}')
        print("--------- Results ---------")
        for result in results:
            print(result)
    
    # TODO: Return results in JSON or as a python list
    return json.dumps({'data' : results, 'state' : 'Mississippi'}, sort_keys=True,
                        indent=None, separators=(',', ': '))
   
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Searches for an active business entity on https://businesssearch.sos.ca.gov/ by \'scraping\' the website.')
    parser.add_argument("searchQuery", help='The name of the business to search for.')
    parser.add_argument("-j", "--json",  help='Print results in JSON', action='store_true')
    args = parser.parse_args()
    main(args)

