#!/usr/bin/env python3

# This script parses bibtex files using bibtex parser and organizes information
# useful for evaluating larege quantities of research papers.
#
# Copyright (c) 2017  James Fraser  <jamey.fraser@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import sys
import getopt
import os
import re

# Bibtex convert to unicode can handle unicode.
# However Mendeley doesn't export to proper unicide format.
# Instead you get additional wrapping around characters such
#    Unicode should be {\'e}
#    Mendeley export different example {\'{i}}
#     Different example not sure what \v does but doesn't seem to pick up in bibtex_parser
#    Extra wrapping of {} needs to be removed

# To bibtex file
#bibtex_str = bibtexparser.dumps(bib_database)


# Note this function strips the extra input from Mendeley
def cleanInput( bibStr ):
    try:
        regStr = r"\{([^{]*)\{(.)\}\}"
        #Reg to replace with accents
        #regWAccents = r"{\1\2}"
        # Reg to strip accents
        regNoAccents = r"\2"
        return re.sub(regStr, regNoAccents, bibStr)
    except:
        print("Something errored:", sys.exc_info()[0])
    return bibStr

def cleanFile( filename ):
    try:
        with open(filename, "r+") as file:
                data = file.read()
                file.seek(0)
                cdata = cleanInput(data)
                file.write(cdata)
                file.truncate()
    except:
        print("Error cleaning data:", sys.exc_info()[0])

def loadFile( filename ):
    try:
        with open(filename) as bibtex_file:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            bib_database = bibtexparser.load(bibtex_file, parser = parser)
            return bib_database.entries
    except:
        print("Bibtex parser errored:", sys.exc_info()[0])
    return  []

def showEntries( entries ):
    print("\n\n********** Start*****************\n\n")
    for e in entries:
        print(e, "\n\n***************************\n\n")
    print("\n\n********** END *****************\n\n")


def showAllKeys(entries):
    print("Available keys:")
    allKeys = {}
    for e in  entries:
        for k in e:
            allKeys[k] = 1

    for ak in allKeys:
        print(ak)

# this function prints usage information
def print_usage():
    print( 'Usage:')
    print()
    print( 'bibtex_extractor.py.py [-t show tags] [-c clean data] [-e entries tags] [-s show input data] -f INPUTFILE')

    return

# main program that takes arguments
def main(argv):

    options = {
       'lowRange': 0,
       'highRange': 10,
       'showFile': False,
       'clean': False,
        'showTags': False,
       'fields':[]
    }

    ifile = ""
    # define command line arguments and check if the script call is valid
    try:
        opts, args = getopt.getopt(argv,'t:c:e:f:s:h',[ 'tag', 'clean', 'entries=','show', 'help'])

        for opt, arg in opts:
            if opt in ('--entries', '-e'):
                for w in arg.split(","):
                    print(w)
                    options['fields'] .append(w)
            elif opt in ('--clean', '-c'):
                options['clean'] = True
            elif opt in ('--tag', '-t'):
                options['showTags'] = True
            elif opt in ('--show', '-s'):
                options['showFile'] = True
            elif opt in ('file', '-f'):
                ifile = arg
                if not (os.path.isfile(ifile)):
                    sys.stderr.write( 'Error. File ' + ifile + ' does not exist.\n' )
                    sys.exit()

    except getopt.GetoptError as err:
        sys.stderr.write('Error. ' + str(err) + '\n')
        print_usage()
        sys.exit(2)  # code 2 means misuse of shell cmd according to Bash docs

    if( ifile != "" ):

        if( options['clean']):
            cleanFile(ifile)

        entries = loadFile(ifile)

        if( options['showTags']):
            showAllKeys(entries)

        if(options['showFile'] == True):
            showEntries(entries)

        for field in options['fields']:
            # Print the field values for each
            for e in  entries:
                if( field in e ):
                    print( e[field] )

    else:
        sys.stderr.write( 'Please provide a bibtex file to evaluate using -f <file>.\n')

if __name__ == '__main__':
    main(sys.argv[1:])