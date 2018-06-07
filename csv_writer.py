#-*- coding: utf-8 -*

import csv

def write_to_csv(csv_file="", header=[], rows=[]):
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows( rows )

def convert_addr_addrgrp_rows( file_parser=None, addrGrp_list=[], netAddr_list=[] ):
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
