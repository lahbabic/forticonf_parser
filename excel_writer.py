#-*- coding: utf-8 -*

class Excel_writer:

    hosts_fieldnames = ['Group', 'Hostname', 'ip/ip_start', 'netmask/ip_end', 'Description']

    services_fieldnames = ['Service Group','service_name', 'tcp_portrange', 'udp_portrange',\
    'sctp_portrange', 'explicit_proxy', 'protocol', 'protocol_number',\
               'visibility', 'icmptype', 'icmpcode', 'category', 'comment']

    policies_fieldnames = ['policy_number', 'srcintf', 'dstintf', 'srcaddr',\
                'dstaddr', 'action', 'schedule', 'service', 'logtraffic',\
                'global_label', 'nat', 'status', 'comments', 'ippool', 'poolname']

    def __init__( self, parser=None, book=None ):
        self.parser = parser
        self.book = book


    def write_row( self, row_num="", rowtw=[], sheet=None ):
        """
            write the specified row to the corresponding sheet
        """
        # rowtw : row to write
        row = sheet.row( row_num )
        for index, value in enumerate( rowtw ):
            row.write( index, value )


    def convert_addr_row( self , group="", member="" ):
        """
            convert address object to writable format and write it
        """
        row = []
        netAddr = None
        netAddr = self.parser.get_netAddr_byName( member )
        if netAddr != None:
            row.append(group)
            row.append( netAddr.get_name() )
            x, y = netAddr.get_addr()
            row.append(x)
            row.append(y)
            row.append( netAddr.get_comment() )
            return row
        return None

    def convert_service_row( self, serviceGrp="", service_name="" ):
        """
            convert service to a row
        """
        row = []
        service = None
        service = self.parser.get_service_byName( service_name )
        if service != None:
            # Create new dictonary with all attributes + Service Group name that
            # the Service belong to
            tmp = dict({'Service Group': serviceGrp} , **(service.get_attrs()))
            for field in self.services_fieldnames:
                if tmp[ field ]:
                    row.append( tmp[ field ] )
                else:
                    row.append("")
            return row
        return None

    def policies_to_file( self ):
        """
            convert all gathered policies into csv format
        """
        self.sheet = self.book.add_sheet("Policies")

        policy_num = 1
        self.write_row( 0, self.policies_fieldnames, self.sheet )
        policies = self.parser.get_list_of_policies()
        for policy in policies:
            if policy != None:
                row = []
                tmp = policy.get_attrs()
                for field in self.policies_fieldnames:
                    if tmp[ field ]:
                        row.append( tmp[ field ] )
                    else:
                        row.append("")
                self.write_row( policy_num , row, self.sheet )
                policy_num += 1


    def objects_to_file( self, first_use=False, type="", root="", objects="" ):
        """
            convert all gathered addresses into csv format
        """
        # first_use is for if we enter this funciton for the first time
        # type is the type of the object
        # root is the parent group
        # the object here can be a group of hosts or
        # a group of services
        if first_use:
            # This variable is to count the number of written rows
            self.row_num = 1
            fieldnames = ""
            if type == "hosts":
                self.sheet = self.book.add_sheet("Hosts")
                fieldnames = self.hosts_fieldnames
            elif type == "services":
                self.sheet = self.book.add_sheet("Services")
                fieldnames = self.services_fieldnames

            self.write_row( 0, fieldnames, self.sheet )

        for object in objects:
            members = object.get_members()
            for member in members:
                tmp = ""
                if member.split("-")[0] == 'g' or member.split("-")[0] == 'sg':
                    # Groups members of a group
                    if type == "hosts":
                        self.objects_to_file( False, "hosts", object.get_name(),\
                            [self.parser.get_addrgrp_byName(member)] )
                    elif type == "services":
                        self.objects_to_file( False, object.get_name() ,\
                            [self.parser.get_serviceGrp_byName(member)] )
                elif root:
                    if type == "hosts":
                        tmp = self.convert_addr_row( root, member )
                    elif type == "services":
                        tmp = self.convert_service_row( root, member)
                else:
                    if type == "hosts":
                        tmp = self.convert_addr_row( object.get_name(), member )
                    elif type == "services":
                        tmp = self.convert_service_row( object.get_name(), member )
                if tmp:
                    self.write_row( self.row_num, tmp, self.sheet )
                    self.row_num += 1
