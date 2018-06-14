#!/usr/bin/env python3
#-*- coding: utf-8 -*

import sys
from optparse import OptionParser
try:
    import xlwt
except ImportError:
    print("No module named 'xlwt'")
    print("Please try to install it using the following command:")
    print("pip3 install xlwt")
    exit(1)

from file.parser import *
from file.excel_writer import *


W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[93m'  # orange
B = '\033[94m'  # blue

def print_done():
    print(W+"["+G+"done"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")
def print_warning():
    print(W+"["+O+"warning"+W+"]")

def missing_arguments( msg="" ):
    print(msg)
    print("Please use -h for more information.")
    print("\t"+sys.argv[0]+ " -h")
    exit("\n")

def main():

    option_parser = OptionParser()
    option_parser.add_option("-f", "--file", dest="config_file",
                      help="fortinet configuration file to parse", metavar="FILE")
    option_parser.add_option("-o", "--output", dest="excel_file",
                      help="excel output FILE which will contain three sheets\
                      ( hosts, services and policies )[default FILE.xls]",
                      metavar="FILE")
    (options, args) = option_parser.parse_args()

    if options.config_file is not None:
        file_parser = File_parser( options.config_file )
        book = xlwt.Workbook()
        excel_writer = Excel_writer( file_parser, book )
    else:
        missing_arguments("You should provide a configuration file as an argument using -f.")

    if options.excel_file is None:
        options.excel_file = options.config_file.split(".")[0]+".xls"

    file_parser.parse("hosts")
    groups = file_parser.get_list_of_addrGrp()
    excel_writer.objects_to_file( True, "hosts", "", groups )

    file_parser.parse("services")
    serviceGs = file_parser.get_list_of_Gservices()
    excel_writer.objects_to_file( True, "services", "", serviceGs )

    file_parser.parse("policies")
    serviceGs = file_parser.get_list_of_policies()
    excel_writer.policies_to_file( )

    print("Writing objects to file "+ options.excel_file + " ...  ",end="")
    book.save( options.excel_file )
    print_done()


if __name__ == '__main__':
    main()
