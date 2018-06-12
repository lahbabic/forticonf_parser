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
            fieldnames = ['Group', 'Hostname', 'ip/ip_start', 'netmask/ip_end', 'Description']
        if objects_type == "service":
            pass

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter( csvfile, fieldnames=fieldnames )
            writer.writeheader()
            writer.writerows( rows )


    def convert_addr_row( self , group="", member="" ):
        """
            function that convert netAddr into a row
            to csv format
            return a row
        """
        row = {}
        netAddr = None
        netAddr = self.parser.get_netAddr_byName( member )
        if netAddr != None:
            row['Group'] = group
            row['Hostname'] = netAddr.get_name()
            row['ip/ip_start'], row['netmask/ip_end'] = netAddr.get_addr()
            row['Description'] = netAddr.get_comment()
            return row
        return None


    def addresses_to_rows( self, root_grp="", groups="" ):
        """
            convert all gathered addresses into csv format
        """
        rows = []
        for group in groups:
            members = group.get_members()
            for member in members:
                if member.split("-")[0] == 'g':
                    # Groups members of a group
                    rows += self.addresses_to_rows( group.get_name(), [self.parser.get_addrgrp_byName(member)] )
                elif root_grp:
                    rows.append( self.convert_addr_row(root_grp, member) )
                else:
                    rows.append( self.convert_addr_row(group.get_name(), member) )

        return rows

    def services_to_rows( self, root_service="", serviceGs="" ):
        """
            convert all gathered services into csv format
        """
        rows = []
        for serviceg in serviceGs:
            print( serviceg )
            services = serviceg.get_services()
            for service in services:
                pass
        return None
