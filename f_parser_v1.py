#!/usr/bin/env python3
#-*- coding: utf-8 -*

import csv, sys
from parser import *
from optparse import OptionParser



W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green

def print_done():
    print(W+"["+G+"done"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")

def write_to_csv(csv_file="", header="", rows=None):
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows( rows )

def convert_netAddr_to_row( group_name="", netAddr=None ):
    """ convert a network address to row in csv format """
    if type(netAddr) is not Network_addr:
        return None
    row = {}
    row['Group'] = group_name
    row['FWaddress name'] = netAddr.get_name()
    row['ip/ip_start'], row['netmask/ip_end'] = netAddr.get_addr()
    row['description'] = netAddr.get_comment()
    return row

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
                      help="csv output FILE ", metavar="FILE")

    (options, args) = option_parser.parse_args()
    if options.csv_file is None:
        options.csv_file = options.config_file.split(".")[0]+".csv"

    print("Parsing configuration file " + options.config_file+" ...  ", end="" )

    #try:
    members = []
    rows = []
    file_parser = File_parser( options.config_file )
    file_parser.parse()
    netAddr_list = file_parser.get_list_of_netAdresses()
    addrGrp_list = file_parser.get_list_of_addrGrp()
    #[ print(obj) for obj in netAddr_list ]
    #[ print(obj) for obj in addrGrp_list ]
    print_done()
    #rows = [ convert_netAddr_to_row( netAddr ) for netAddr in netAddr_list ]
    #[ print(row) for row in rows ]
    print("Creating csv file : " + options.csv_file +"  ...", end="")
    rows = [ convert_netAddr_to_row( group.get_name(), file_parser.get_netAddr_byName(member) )
                for group in addrGrp_list
                        for member in group.get_members()]

    #csv_file = config_file.split(".")[0]+".csv"
    header =  ['Group', 'FWaddress name', 'ip/ip_start', 'netmask/ip_end', 'description']
    write_to_csv( options.csv_file, header, rows )
    #except:
    #    print_err()
    #    exit(1)


    print_done()


if __name__ == '__main__':
    main()
