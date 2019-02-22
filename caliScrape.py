#!/usr/bin/env python3

import mechanize
import argparse
import re
import json
from urllib.parse import quote
from bs4 import BeautifulSoup

MAX_SIZE = 5
#TODO MUST BE REFACTORED!
#TODO DON'T turn this in without refactoring! 
#TODO Merge with Florida search
def searchState(searchQuery):
    
    browser = mechanize.Browser()
    formattedInput = quote(searchQuery)
    #print('url: ', f'https://businesssearch.sos.ca.gov/CBS/SearchResults?filing=False&SearchType=CORP&SearchCriteria={formattedInput}&SearchSubType=Keyword') 
    #TODO: Remove hard coded url 
    response = browser.open(f'https://businesssearch.sos.ca.gov/CBS/SearchResults?filing=False&SearchType=CORP&SearchCriteria={formattedInput}&SearchSubType=Keyword')
    html = response.read() # TODO: FIND OUT WHY THIS WORKS!!!!
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')  
    tags = soup.find_all('td')
    activeBusinesses = []  
    #print(tags)

    for index, tag in enumerate(tags):
        # Get the string content from the html tag...
        tagString = str(tag.string).lstrip() if tag.string != None else ""
        
        #NOTE: len() on a list is an O(1) operation... 
        if(len(activeBusinesses) < MAX_SIZE and re.search('Active', tagString, re.I)):
            activeBusinesses.append(tags[index + 1]['data-order'])
            #print(tags[index + 1]['data-order'])
                 
    return activeBusinesses

def main(args):
    results = searchState(args.searchQuery)

    # Output results
    if(args.json):
        print(json.dumps({'data' : results, 'state' : 'California'}, sort_keys=True,
                         indent=4, separators=(',', ': ')))
    else:
        print(f'Found {len(results)} active businesses while searching for {args.searchQuery}')
        print("--------- Results ---------")
        for result in results:
            print(result)
    
    # TODO: Return results in JSON or as a python list
    return json.dumps({'data' : results, 'state' : 'California'}, sort_keys=True,
                        indent=None, separators=(',', ': '))
   
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Searches for an active business entity on https://businesssearch.sos.ca.gov/ by \'scraping\' the website.')
    parser.add_argument("searchQuery", help='The name of the business to search for.')
    parser.add_argument("-j", "--json",  help='Print results in JSON', action='store_true')
    args = parser.parse_args()
    main(args)



