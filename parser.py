#-*- coding: utf-8 -*

from network.FWaddress import *
from network.FWaddrgrp import *

class File_parser():
    """ parse a configuration file and create needed objects"""
    def __init__(self, file_name=""):
        self.file_name = file_name
        # list containing Network_addr objects
        self.list_of_netAddresses = []
        # list containing Address_group objects
        self.list_of_addrGrp = []
        # list containing the members of an group
        self.list_of_members = []
        self.conf_addr = False
        self.conf_addrgrp = False
        # name of network address or of the address group
        self.name = ""
        self.addrtype = ""
        self.comment = ""
        # network ip address
        self.x = ""
        # network mask
        self.y = ""

    def get_line_from_file( self, file_name="", mode='r' ):
        """ function that returns line by line during file reading """
        try:
            file = open( str(file_name), mode, encoding='utf-8')
            for line in file:
                yield line
            file.close()
        except IOError:
            exit(1)

    def config_action( self, obj_to_conf='' ):
        if obj_to_conf == 'address':
            self.conf_addr = True
        elif obj_to_conf == 'addrgrp':
            self.conf_addrgrp = True

    def edit_action( self, args=[] ):
        self.name = ' '.join(args).strip('"')

    def set_action( self, args=[] ):
        if self.conf_addr:
            if args[0] == 'subnet':
                self.addrtype = 'ipmask'
                # network ip address
                self.x = args[1]
                # network mask
                self.y = args[2]
            elif args[0] == 'type':
                if args[1] == 'ipmask':
                    self.addrtype = args[1]
                elif args[1] == 'iprange':
                    self.addrtype = args[1]
            elif args[0] == 'start-ip':
                self.x = args[1]
            elif args[0] == 'end-ip':
                self.y = args[1]
            elif args[0] == 'comment':
                # pop the 'comment' keyword
                args.pop(0)
                self.comment = ' '.join(args)
        if self.conf_addrgrp:
            # pop the 'member' keyword
            args.pop(0)
            self.list_of_members = args

    def next_action( self ):
        """ create the correspondent objects with the gathered information
            and store them """
        if self.conf_addr:
            self.net_addr = Network_addr( self.name, self.addrtype )
            self.net_addr.set_addr(self.x, self.y)
            if self.comment != "":
                self.net_addr.set_comment( self.comment )
                self.comment = ""
            # append the newly created network address in the tuple
            self.list_of_netAddresses.append( self.net_addr )
        if self.conf_addrgrp:
            self.addr_grp = Address_group( self.name )
            #ajout de tout les membres à l'objet addr_grp
            [ self.addr_grp.add_member( member.strip('"') )
                                for member in self.list_of_members ]
            self.list_of_addrGrp.append( self.addr_grp )

    def end_action( self ):
        """ reinit all attributes """
        self.addrtype, self.name, self.comment = "", "", ""
        self.x, self.y = "", ""
        self.conf_addr = False
        self.conf_addrgrp = False
        self.list_of_members = []

    def parse( self ):
        """ read lines from config file and parse information """
        for line in self.get_line_from_file( self.file_name ):
            try:
                action, *args = line.split()
            except:
                pass

            if action == 'config':
                self.config_action( args[-1] )
            elif action == 'edit':
                self.edit_action( args )
            elif action == 'set':
                self.set_action( args )
            elif action == 'next':
                self.next_action( )
            elif action == 'end':
                self.end_action( )

    def get_netAddr_byName( self, name="" ):
        for net_addr in self.list_of_netAddresses:
            if net_addr.get_name() == name:
                return net_addr


    def get_list_of_netAdresses( self ):
        """ return a list of network address objects """
        return self.list_of_netAddresses

    def get_list_of_addrGrp( self ):
        """ return a list of address group objects """
        return self.list_of_addrGrp
