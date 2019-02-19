#!/usr/bin/env python3

'''
Author: Felipe Zuniga Calier (Felipe-ZC)  

A python script that scrapes the HTML on search.sunbiz.org to determine if a
given business (in Florida) is an active business entity. 
'''

import re
import requests
import json
import argparse
from bs4 import BeautifulSoup
from urllib.parse import quote

# TODO: XML Bombs
# TODO: Command Line option to match results with searchQuery instead returning
# all active businesses found?
# TODO: 'import from' on all imports?
# TODO: Review command line options and arguments
def searchSunBiz(searchQuery):

    # f strings are a new construct introduced in python 3.6, allows for string interpolation like in Node and other languages.
    formattedInput = quote(searchQuery)
    link = f'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder={formattedInput.upper()}&searchTerm={formattedInput}'
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('td')
    activeBusinesses = []
 
    '''
    Look for a match in each <td> element, if a match is found on index i then
    the <td> element that describes the business' status is found on index i +
    2. 

    This is a pretty basic approach to the problem but most of this is hacked
    af, needs review!
    '''
    # Find all active business entities...
    # TODO: MAKE THIS READABLE!!!! WTF!!!!
    for index, tag in enumerate(tags):
        if(tag.find('a')): 
            # TODO: CHECK FOR OUT OF BOUNDS YOU DICK!
            #if(re.match(formattedInput, str(tag.find('a').string), re.I) and re.match('Active', str(tags[index + 2].string))):
            if(re.match('Active', str(tags[index + 2].string))):
                activeBusinesses.append(tag.find('a').string)
             
    return activeBusinesses


'''
Return a list of results, let user
choose from list in frontend.
'''
def main(args):
    results = searchSunBiz(args.businessName)
    
    # Output results
    if(args.json):
        print(json.dumps({'data' : results}, sort_keys=True,
                         indent=4, separators=(',', ': ')))
    else:
        print(f'Found {len(results)} active businesses while searching for {args.businessName}')
        print("--------- Results ---------")
        for result in results:
            print(result)
    
    # Return results in JSON or as a python list
    return json.dumps({'data' : results}, sort_keys=True,
                        indent=None, separators=(',', ': '))

# Parse command line arguments and search sunbiz.org    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Searches for an active business entity on search.sunbiz.org by \'scraping\' the website.')
    parser.add_argument("businessName", help='The name of the business to search for.') 
    parser.add_argument("-j", "--json",  help='Print results in JSON', action='store_true')
    args = parser.parse_args()
    main(args)
