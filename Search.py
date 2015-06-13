#!/usr/bin/env python

import glob
import os
import sys
import webbrowser
import os

from distutils.util import strtobool
from modules.db_manager import DB_Manager
from modules.reporting import search_report


def open_file_input(cli_parsed):
    files = glob.glob(os.path.join(cli_parsed.d, 'search.html'))
    if len(files) > 0:
        print 'Would you like to open the report now? [Y/n]',
        while True:
            try:
                response = raw_input().lower()
                if response is "":
                    return True
                else:
                    return strtobool(response)
            except ValueError:
                print "Please respond with y or n",
    else:
        print '[*] No report files found to open, perhaps no hosts were successful'
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print '[*] Usage: python Search.py <dbpath> <searchterm>'
        sys.exit()
    db_path = sys.argv[1]
    if not os.path.isfile(db_path):
        print '[*] No valid db path provided'
    search_term = sys.argv[2]
    dbm = DB_Manager(db_path)
    dbm.open_connection()
    results = dbm.search_for_term(search_term)
    if len(results) == 0:
        print 'No results found!'
        sys.exit()
    else:
        print 'Found {0} Results!'.format(str(len(results)))
    cli_parsed = dbm.get_options()
    cli_parsed.results = 25
    oldfiles = glob.glob(os.path.join(cli_parsed.d, "*search*.html"))
    for f in oldfiles:
        os.remove(f)
    search_report(cli_parsed, results, search_term)
    newfiles = glob.glob(os.path.join(cli_parsed.d, "*search*.html"))
    if open_file_input(cli_parsed):
        for f in newfiles:
            webbrowser.open(f)
    sys.exit()
