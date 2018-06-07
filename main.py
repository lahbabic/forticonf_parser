#!/usr/bin/env python3
#-*- coding: utf-8 -*

import sys
from parser import *
from csv_writer import *
from optparse import OptionParser


W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m'  # blue

def print_done():
    print(W+"["+G+"done"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")


def main():
    if len(sys.argv) < 2:
        print("You should provide a configuration file as an argument.")
        print("Please use -h for more information.")
        print("\t"+sys.argv[0]+ " -h")
        exit("\n")

    option_parser = OptionParser()
    option_parser.add_option("-f", "--file", dest="config_file",
                      help="fortinet configuration file to parse", metavar="FILE")
    option_parser.add_option("-o", "--output", dest="csv_file",
                      help="csv output FILE, [default FILE.csv] ", metavar="FILE")

    (options, args) = option_parser.parse_args()
    if options.csv_file is None:
        options.csv_file = options.config_file.split(".")[0]+".csv"

    print("Parsing configuration file " + options.config_file+" ...  ", end="" )
    file_parser = File_parser( options.config_file )
    file_parser.parse()
    netAddr_list = file_parser.get_list_of_netAdresses()
    addrGrp_list = file_parser.get_list_of_addrGrp()
    print_done()

    print("Creating csv file : " + options.csv_file +"  ...", end="")
    """ for each address group, take their members and convert them into
        csv format stored as rows"""

    rows = convert_addr_addrgrp_rows( file_parser, addrGrp_list, netAddr_list )

    header =  ['Group', 'address/addrgrp', 'ip/ip_start', 'netmask/ip_end', 'description']
    write_to_csv( options.csv_file, header, rows )
    print_done()

if __name__ == '__main__':
    main()
