#!/usr/bin/env python3
#-*- coding: utf-8 -*

import sys
from optparse import OptionParser


from file.parser import *
from file.excel_writer import *
from file.mgmt_cli_writer import *

from print_x import *


def error_msg( msg="" ):
    print(msg)
    print("Please use -h for more information.")
    print("\t"+sys.argv[0]+ " -h")
    exit("\n")

def main():

    option_parser = OptionParser()
    option_parser.add_option("-f", "--file", dest="config_file",
                      help="Fortinet configuration file to parse", metavar="FILE")
    option_parser.add_option("-e", "--excel_file", dest="excel_file",
                      help="Excel output FILE which will contains three sheets\
                      ( hosts, services and policies )[default FILE.xls]",
                      metavar="FILE")
    option_parser.add_option("-m", "--mgmt_cli", dest="mgmt_cli_file",
                      help="Output FILE which will contains\
                      mgmt_cli commands",
                      metavar="FILE")
    (options, args) = option_parser.parse_args()

    file_format = None

    if options.excel_file is not None and options.mgmt_cli_file is not None:
        error_msg("To many arguments.")
    elif options.excel_file is None and options.mgmt_cli_file is None:
        print(options.config_file)
        options.excel_file = options.config_file.split(".")[0]+".xls"
        file_format = (options.excel_file, "excel")
    elif options.excel_file is not None and options.mgmt_cli_file is None:
        file_format = (options.excel_file, "excel")
    elif options.mgmt_cli_file is not None and options.excel_file is None:
        file_format = (options.mgmt_cli_file, "mgmt_cli")
    else:
        error_msg("Failed to parse arguments.")

    if options.config_file is not None:
        file_parser = File_parser( options.config_file )
    else:
        error_msg("You should provide a configuration file as an argument using -f.")

    file_parser.parse()

    if file_format[1] == "excel":
        excel_writer = Excel_writer( file_parser, file_format[0] )
        excel_writer.write_objects()

    elif file_format[1] == "mgmt_cli":
        mgmt_cli_writer = Mgmt_cli_writer( file_parser, file_format[0] )
        mgmt_cli_writer.write_specific_policies()


if __name__ == '__main__':
    try:
        main()
    except Exception as im:
        print_err()
        print(im)
