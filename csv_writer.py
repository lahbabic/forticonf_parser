#-*- coding: utf-8 -*

import csv
from parser import *

class Csv_writer:

    def __init__( self, parser=None ):
        self.parser = parser

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


    def convert_group_rows( self , parent_group="", group=None ):
        """
            function that take an Addrgroup and convert each member into a row
            to csv format
            return a list of rows
        """
        rows = []
        members = group.get_members()
        for member in members:
            row = {}
            netAddr = self.parser.get_netAddr_byName( member )
            if netAddr != None:
                row['Group'] = parent_group
                row['address/addrgrp'] = netAddr.get_name()
                row['ip/ip_start'], row['netmask/ip_end'] = netAddr.get_addr()
                row['description'] = netAddr.get_comment()
                rows.append( row )
        return rows

    def get_addr_rows( self ):
        """
            convert all gathered addresses into csv format
        """

        """ revoir ici """
        rows = []
        groups = self.parser.get_list_of_addrGrp()
        for group in groups:
            members = group.get_members()
            for member in members:
                if member.split("-")[0] == 'g':
                    print(O+"group: "+W+member)
                    rows += self.convert_group_rows( group.get_name(),\
                            self.parser.get_addrgrp_byName( member ))
                else:
                    print(O+"host: "+W+member)
                    rows += self.convert_group_rows( group.get_name(), group )
        return rows

        
