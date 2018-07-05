#-*- coding: utf-8 -*


class Excel_writer:

    hosts_fieldnames = ['Hostname', 'Member of groups',\
            'ip/ip_start', 'netmask/ip_end', 'Description']

    services_fieldnames = ['service name','member of groups', 'tcp_portrange',\
     'udp_portrange', 'sctp_portrange', 'explicit_proxy', 'protocol',\
      'protocol_number','visibility', 'icmptype', 'icmpcode', 'category', 'comment']

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

    def policies_to_file( self ):
        """
            write policy objects to excel file
        """
        self.sheet = self.book.add_sheet("Policies")

        policy_num = 1
        self.write_row( 0, self.policies_fieldnames, self.sheet )
        policies = self.parser.get_list_of_policies()
        for policy in policies:
            if policy != None:
                row = policy.convert_to_row()
                self.write_row( policy_num , row, self.sheet )
                policy_num += 1


    def objects_to_file( self, type="", objects="" ):
        """
            write objects( Network_addr| services ) to excel file
        """
        # The objects here can be hosts or services
        # This variable is to count the number of written rows
        self.row_num = 1
        fieldnames = ""
        if not objects:
            return 1
        if objects[0].__class__.__name__ == "Network_addr":
            self.sheet = self.book.add_sheet( "Hosts" )
            fieldnames = self.hosts_fieldnames
        elif objects[0].__class__.__name__ == "Service":
            self.sheet = self.book.add_sheet( "Services" )
            fieldnames = self.services_fieldnames

        self.write_row( 0, fieldnames, self.sheet )

        for obj in objects:
            tmp = None
            # obj = self.parser.get_obj_byName( type, member )
            if obj:
                tmp = obj.convert_to_row( )

            if tmp:
                self.write_row( self.row_num, tmp, self.sheet )
                self.row_num += 1
