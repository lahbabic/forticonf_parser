#-*- coding: utf-8 -*

from network.FWaddress import *
from service.service import *

W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[93m'  # orange
B = '\033[94m'  # blue


def print_done():
    print(W+"["+G+"done"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")
def print_warning():
    print(W+"["+O+"warning"+W+"]")

class File_reader():
    """
        read lines from file, return lines until 'end' keyword
        if action is : 'config firewall object'
        object can be [address, addrgrp, policy, service, servicegrp]
    """
    def __init__( self, file_name="" ):
        self.file_name = file_name

    def get_line_from_file( self ):
        """ function that returns line by line during file reading """
        try:
            file = open( str( self.file_name ), 'r', encoding='utf-8')
            for line in file:
                yield line
            file.close()
        except OSError:
            print_err()
            print("Failed to process file "+B+ self.file_name +W+"\n")
            exit(1)

    def get_objects( self, object='' ):
        """
            return a list containing all objects after 'config firewall object'
            if object in [address, addrgrp, policy, service, servicegrp]
        """
        if object not in ['address', 'addrgrp', 'policy', 'service custom', 'service group']:
            print_warning()
            print("Can't parse the object "+B+object+W+" from the file, not implemented yet")
            return None
        # set to True if 'object' is found
        object_found = False
        lines, service = [], []

        if 'service' in object:
            service = object.split()

        for line in self.get_line_from_file():
            try:
                action, *args = line.split()
            except:
                pass

            if action == 'config' and args[0] == 'firewall':
                if len(service) == 2\
                        and service[0] and service[1] in args\
                        or object in args:
                    object_found = True
            elif action == 'end':
                object_found = False

            if object_found == True:
                lines.append( line.strip("\n").strip() )
        print_done()
        return lines


class File_parser():
    """ parse a configuration file and create needed objects """

    def __init__(self, file_name=""):
        self.file_reader = File_reader( file_name )
        # list containing Network_addr objects
        self.list_of_netAddresses = []
        # list containing Address_group objects
        self.list_of_addrGrp = []
        # list containing the members of an group
        self.list_of_members = []
        # list containing service objects
        self.list_of_services = []


    def create_addrObj( self, lines=[] ):
        """
            create network address objects from lines
            'firewall address'
        """
        if not lines:
            return None

        net_addr = None
        addrtype, name, x, y = "", "", "", ""
        command, comment = "", ""
        args = []

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                name = args[0].strip('"')
            elif command == 'set':
                if args[0] == 'subnet':
                    addrtype = 'ipmask'
                    # network ip address
                    x = args[1]
                    # network mask
                    y = args[2]
                elif args[0] == 'type':
                    if args[1] in ['ipmask', 'iprange']:
                        addrtype = args[1]
                elif args[0] == 'start-ip':
                    x = args[1]
                elif args[0] == 'end-ip':
                    y = args[1]
                elif args[0] == 'comment':
                    # pop the 'comment' keyword
                    args.pop(0)
                    comment = ' '.join(args)
            elif command == 'next':
                if addrtype:
                    net_addr = Network_addr( name, addrtype )
                    net_addr.set_addr( x, y )
                    if comment != "":
                        net_addr.set_comment( comment )
                        comment = ""
                    # append the newly created network address into the list
                    self.list_of_netAddresses.append( net_addr )
                    # reinit variables
                    net_addr = None
                    addrtype, name, x, y = "", "", "", ""
                    command, comment = "", ""
                    args = []
        print_done()

    def create_addrgrpObj( self, lines=[] ):
        """ create 'firewall addrgrp' objects """
        if not lines:
            return None

        command, name, comment = "", "", ""
        args, addrgrp_list = [], []

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                name = args[0].strip('"')
            elif command == 'set':
                if args[0] == "member":
                    # pop 'member' keyword
                    args.pop(0)
                    [ addrgrp_list.append( member ) for member in args ]
                elif args[0] == "comment":
                    # pop 'comment' keyword
                    args.pop(0)
                    comment = ' '.join(args).strip('"')
            elif command == "next":
                addr_grp = Address_group( name )
                [ addr_grp.add_member(member.strip('"')) for member in addrgrp_list ]
                addr_grp.set_comment( comment )
                self.list_of_addrGrp.append( addr_grp )
                # reinit variables
                command, name, comment = "", "", ""
                args, addrgrp_list = [], []
        print_done()

    def create_serviceCObj( self, lines=[] ):
        """ create 'firewall service custom' objects """
        if not lines:
            return None

        command = ""
        args, service_list = [], []
        service = {}
        implemented_fields = ['name', 'explicit-proxy', 'protocol', 'protocol-number',
                   'visibility', 'icmptype', 'icmpcode']

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                service['name'] = args[0].strip('"')
            elif command == 'set':
                try:
                    if args[0] == 'tcp-portrange' or args[0] == 'udp-portrange':
                        portrange_type = args[0]
                        args.pop(0)
                        service[ portrange_type ] = args
                    elif args[0] in implemented_fields:
                        service[ args[0] ] = args[1]
                    else:
                        print_warning()
                        print("Can't set the field "+B+args[0]+W+", not implemented yet")
                except:
                    pass
            elif command == 'unset':
                """ need to implement this case"""
                pass
            elif command == "next":
                service_Obj = None
                service_Obj = Service( service )
                self.list_of_services.append( service_Obj )
                service.clear()
        print_done()

    def parse( self ):
        print("File parsing for the"+B+" address"+W+" objects ...  ", end="" )
        addrs_lines = self.file_reader.get_objects( 'address' )

        print("Creating address objects ...  ", end="" )
        self.create_addrObj( addrs_lines )

        print("File parsing for the"+B+" addrgrp"+W+" objects ...  ", end="" )
        addrgrp_lines = self.file_reader.get_objects( 'addrgrp' )

        print("Creating addrgrp objects ...  ", end="" )
        self.create_addrgrpObj( addrgrp_lines )

        print("File parsing for the"+B+" service custom"+W+" ...  ", end="" )
        serviceC_lines = self.file_reader.get_objects( 'service custom' )

        print("Creating service objects ...  ", end="" )
        self.create_serviceCObj( serviceC_lines )


    def get_netAddr_byName( self, name="" ):
        """ return netAddr object that has the name given in argument"""
        for net_addr in self.list_of_netAddresses:
            if net_addr.get_name() == name:
                return net_addr
        return None

    def get_addrgrp_byName( self, name="" ):
        """ return addrgrp object that has the name given in argument"""
        for addrgrp in self.list_of_addrGrp:
            if addrgrp.get_name() == name:
                return addrgrp
        return None

    def get_list_of_netAdresses( self ):
        """ return a list of network address objects """
        return self.list_of_netAddresses

    def get_list_of_addrGrp( self ):
        """ return a list of address group objects """
        return self.list_of_addrGrp
