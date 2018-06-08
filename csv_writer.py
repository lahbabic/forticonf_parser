#-*- coding: utf-8 -*

import csv


class Csv_writer:
    def __init__( self ):
        pass

    @staticmethod
    def write_to_csv( self, csv_file="", objects_type="", rows=[] ):
        """ write to csv file """
        fieldnames = []
        if objects_type == "address":
            fieldnames = ['Group', 'address/addrgrp', 'ip/ip_start', 'netmask/ip_end', 'description']
        if objects_type == "service":
            pass

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter( csvfile, fieldnames=fieldnames )
            writer.writeheader()
            writer.writerows( rows )

    @staticmethod
    def convert_addr_row( self, file_parser=None, addrgrp=None, netAddr_list=[] ):
        row = {}
        for member in netAddr_list:
            netAddr = file_parser.get_netAddr_byName( member )
            if netAddr != None:
                row['Group'] = addrgrp.get_name()
                row['address/addrgrp'] = netAddr.get_name()
                row['ip/ip_start'], row['netmask/ip_end'] = netAddr.get_addr()
                row['description'] = netAddr.get_comment()
                yield row
            elif member.split("-")[0] == 'g':
                addrgrp = file_parser.get_addrgrp_byName(member)
                for submember in addrgrp.get_members():
                    row = {}
                    netAddr = file_parser.get_netAddr_byName( submember )
                    if netAddr != None:
                        row['Group'] = group.get_name()
                        row['address/addrgrp'] = netAddr.get_name()
                        row['ip/ip_start'], row['netmask/ip_end'] = netAddr.get_addr()
                        row['description'] = netAddr.get_comment()
                        yield row

    def convert_service_row( self ):
        pass
