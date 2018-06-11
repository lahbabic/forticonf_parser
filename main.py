#!/usr/bin/env python3
#-*- coding: utf-8 -*

import sys
from parser import *
from csv_writer import *
from optparse import OptionParser


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
    option_parser.add_option("-H", "--hosts", dest="csv_hosts",
                      help="csv output FILE for hosts and groups [default FILE_hosts.csv]",
                      metavar="FILE")
    option_parser.add_option("-s", "--services", dest="csv_services",
                      help="csv output FILE for services [default FILE_services.csv]",
                      metavar="FILE")

    (options, args) = option_parser.parse_args()

    if options.config_file is not None:
        file_parser = File_parser( options.config_file )
        csv_writer = Csv_writer( file_parser )
    else:
        missing_arguments("You should provide a configuration file as an argument using -f.")

        ''' extract addresses and groups objects'''
    if options.csv_hosts is not None:
        file_parser.parse("hosts")
        """ for each address group, take their members and convert them into
            csv format stored as rows"""
        groups = file_parser.get_list_of_addrGrp()
        rows = csv_writer.addresses_to_rows( "", groups )
        print("Writing hosts objects into csv file : "+ options.csv_hosts +"  ...  ", end="")
        csv_writer.write_to_csv( options.csv_hosts, "address", rows )
        print_done()
        ''' extract services (service custom and service group)'''
    elif options.csv_services is not None:
        file_parser.parse("services")
        [print(service) for service in file_parser.get_list_of_Cservices()]
        #[print(Sgrp) for Sgrp in file_parser.get_list_of_Gservices()]
    else:
        missing_arguments("Please specify what type of objects you want to extract.")




if __name__ == '__main__':
    main()
