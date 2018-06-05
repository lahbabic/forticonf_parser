#-*- coding: utf-8 -*

from network.FWaddress import *
from network.FWaddrgrp import *

W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m'  # blue

def print_done():
    print(W+"["+G+"done"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")

class File_parser():
    """ parse a configuration file and create needed objects """
    def __init__(self, file_name=""):
        self.file_name = file_name
        # list containing Network_addr objects
        self.list_of_netAddresses = []
        # list containing Address_group objects
        self.list_of_addrGrp = []
        # list containing the members of an group
        self.list_of_members = []
        # address | addrgrp | policy
        self.obj_to_conf = ""
        # name of network address or of the address group
        self.name = ""
        self.addrtype = ""
        self.comment = ""
        # network ip address
        self.x = ""
        # network mask
        self.y = ""
        # check if we are configuring Firewall
        self.fw = False

    def get_line_from_file( self, file_name="", mode='r' ):
        """ function that returns line by line during file reading """
        try:
            file = open( str(file_name), mode, encoding='utf-8')
            for line in file:
                yield line
            file.close()
        except OSError:
            print_err()
            print("Failed to open file "+B+ file_name +W+"\n")
            exit(1)

    def config_action( self, obj_to_conf='' ):
        if obj_to_conf in ['address', 'addrgrp']:
            self.obj_to_conf = obj_to_conf
        else:
            print("\nObject "+B+ obj_to_conf+W+" unknown from the parser probably not yet implemented.")

    def edit_action( self, args=[] ):
        if self.obj_to_conf in ['address', 'addrgrp']:
            self.name = ' '.join(args).strip('"')
        else:
            pass

    def set_action( self, args=[] ):
        if self.obj_to_conf == 'address':
            if args[0] == 'subnet':
                self.addrtype = 'ipmask'
                # network ip address
                self.x = args[1]
                # network mask
                self.y = args[2]
            elif args[0] == 'type':
                if args[1] in ['ipmask', 'iprange']:
                    self.addrtype = args[1]
            elif args[0] == 'start-ip':
                self.x = args[1]
            elif args[0] == 'end-ip':
                self.y = args[1]
            elif args[0] == 'comment':
                # pop the 'comment' keyword
                args.pop(0)
                self.comment = ' '.join(args)
        elif self.obj_to_conf == 'addrgrp':
            # pop the 'member' keyword
            args.pop(0)
            self.list_of_members = args
        else:
            pass

    def next_action( self ):
        """ create the correspondent objects with the gathered information
            and store them """
        if self.obj_to_conf == 'address':
            if self.addrtype:
                self.net_addr = Network_addr( self.name, self.addrtype )
                self.net_addr.set_addr(self.x, self.y)
                if self.comment != "":
                    self.net_addr.set_comment( self.comment )
                    self.comment = ""
                # append the newly created network address into the list
                self.list_of_netAddresses.append( self.net_addr )
        elif self.obj_to_conf == 'addrgrp':
            self.addr_grp = Address_group( self.name )
            # append all members into addr_grp object
            [ self.addr_grp.add_member( member.strip('"') )
                                for member in self.list_of_members ]
            self.list_of_addrGrp.append( self.addr_grp )
        else:
            pass

    def end_action( self ):
        """ reinit all attributes """
        if self.obj_to_conf in ['address', 'addrgrp']:
            self.addrtype, self.name, self.comment = "", "", ""
            self.x, self.y = "", ""
            self.obj_to_conf = ""
            self.fw = False
            self.list_of_members = []
        else:
            pass

    def parse( self ):
        """ read lines from config file and parse information """
        for line in self.get_line_from_file( self.file_name ):
            try:
                action, *args = line.split()
            except:
                pass

            if action == 'config':
                if len(args) > 1:
                    if args[0] == 'firewall':
                        self.fw = True
                        self.config_action( args[-1] )
            elif self.fw and action == 'edit':
                self.edit_action( args )
            elif self.fw and action == 'set':
                self.set_action( args )
            elif self.fw and action == 'next':
                self.next_action( )
            elif self.fw and action == 'end':
                self.end_action( )

    def get_netAddr_byName( self, name="" ):
        """ return netAddr object that has the name given in argument"""
        for net_addr in self.list_of_netAddresses:
            if net_addr.get_name() == name:
                return net_addr


    def get_list_of_netAdresses( self ):
        """ return a list of network address objects """
        return self.list_of_netAddresses

    def get_list_of_addrGrp( self ):
        """ return a list of address group objects """
        return self.list_of_addrGrp
