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
    option_parser.add_option("-p", "--policies", dest="csv_policies",
                      help="csv output FILE for policies [default FILE_policies.csv]",
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
    if options.csv_services is not None:
        file_parser.parse("services")
        serviceGs = file_parser.get_list_of_Gservices()
        rows = csv_writer.services_to_rows( "", serviceGs )
        print("Writing services objects into csv file : "+ options.csv_services +"  ...  ", end="")
        csv_writer.write_to_csv( options.csv_services, "service", rows )
        print_done()
    if options.csv_policies is not None:
        file_parser.parse("policies")
        rows = csv_writer.policies_to_rows()
        print("Writing policy objects into csv file : "+ options.csv_policies +"  ...  ", end="")
        csv_writer.write_to_csv( options.csv_policies, "policy", rows )
        print_done()


if __name__ == '__main__':
    main()
