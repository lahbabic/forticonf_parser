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
        elif objects_type == "service":
            fieldnames = ['Service Group','service_name', 'tcp_portrange', 'udp_portrange',\
            'sctp_portrange', 'explicit_proxy', 'protocol', 'protocol_number',\
                       'visibility', 'icmptype', 'icmpcode', 'category', 'comment']
        elif objects_type == "policy":
            fieldnames = ['policy_number', 'srcintf', 'dstintf', 'srcaddr',\
                        'dstaddr', 'action', 'schedule', 'service', 'logtraffic',\
                        'global_label', 'nat', 'status', 'comments', 'ippool', 'poolname']

    #    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter( csvfile, fieldnames=fieldnames )
            writer.writeheader()
            writer.writerows( rows )
    #    except:
    #        print_err()

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
                    tmp = self.convert_addr_row(root_grp, member)
                    if tmp:
                        rows.append( tmp )
                else:
                    tmp = self.convert_addr_row(group.get_name(), member)
                    if tmp:
                        rows.append( tmp )
        return rows

    def convert_service_row( self, serviceGrp="", service_name="" ):
        """
            convert service to a row
        """
        row = {}
        service = None
        service = self.parser.get_service_byName( service_name )
        if service != None:
            # Create new dictonary with all attributes + Service Group name that
            # the Service belong to
            row = dict({'Service Group': serviceGrp} , **(service.get_attrs()))
            return row
        return None

    def services_to_rows( self, root_serviceG="", serviceGs="" ):
        """
            convert all gathered services into csv format
        """
        rows = []
        for serviceg in serviceGs:
            services = serviceg.get_services()
            for service in services:
                if service:
                    if service.split("-")[0] == 'sg':
                        rows += self.services_to_rows( serviceg.get_name() ,\
                        [self.parser.get_serviceGrp_byName(service)] )
                    elif root_serviceG:
                        tmp = self.convert_service_row(root_serviceG, service)
                        if tmp:
                            rows.append( tmp )
                    else:
                        tmp = self.convert_service_row(serviceg.get_name(), service)
                        if tmp:
                            rows.append( tmp )
        return rows


    def policies_to_rows( self ):
        """
            convert all gathered policies into csv format
        """
        rows = []
        policies = self.parser.get_list_of_policies()
        for policy in policies:
            if policy != None:
                rows.append( policy.get_attrs() )
        return rows
