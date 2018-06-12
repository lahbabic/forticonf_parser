#-*- coding: utf-8 -*

import csv
from parser import *

"""
    need to update the convertion form addresses to rows:
    check for address if it belong to a group not the opposite
    because if the address do not belong to a group it will not appeare in
    the csv file
"""
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

    def convert_service_row( self, serviceGrp="", service_name="" ):
        """
            convert service to a row
        """
        row = {}
        service = None
        service = self.parser.get_service_byName( service_name )
        print(service)
        if service != None:
            row['Service Group'] = serviceGrp
            row['service'] = service.get_name()
            return row
        return None

    def services_to_rows( self, root_service="", serviceGs="" ):
        """
            convert all gathered services into csv format
        """
        rows = []
        for serviceg in serviceGs:
            #print( serviceg )
            services = serviceg.get_services()
            for service in services:
                if service.split("-")[0] == 'sg':
                    pass
                elif root_service:
                    pass
                else:
                    rows.append( self.convert_service_row(serviceg.get_name(), service) )

        #print(rows)
        return rows
