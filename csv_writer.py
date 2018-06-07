#-*- coding: utf-8 -*

import csv


class Csv_writer:
    def __init__( self, csv_file="" ):
        self.csvfile = csv_file

    def write_to_csv( self, objects_type="", rows=[] ):
        """ write to csv file """
        if objects_type == "address":
            fieldnames = ['Group', 'address/addrgrp', 'ip/ip_start', 'netmask/ip_end', 'description']
        if objects_type == "service":
            pass

        with open(self.csvfile, 'w', newline='') as csvfile:
            writer = csv.DictWriter( csvfile, fieldnames=fieldnames )
            writer.writeheader()
            writer.writerows( rows )

    def convert_addr_addrgrp_rows( self, file_parser=None, addrGrp_list=[], netAddr_list=[] ):
        rows = []
        for group in addrGrp_list:
            for member in group.get_members():
                row = {}
                netAddr = file_parser.get_netAddr_byName( member )
                if netAddr != None:
                    row['Group'] = group.get_name()
                    row['address/addrgrp'] = netAddr.get_name()
                    row['ip/ip_start'], row['netmask/ip_end'] = netAddr.get_addr()
                    row['description'] = netAddr.get_comment()
                    rows.append( row )
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
                            rows.append( row )
        return rows
