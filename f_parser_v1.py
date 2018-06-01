#!/usr/bin/env python3
#-*- coding: utf-8 -*

import csv, sys
import ipaddress

W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green

def print_done():
    print(W+"["+G+"done"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")

def get_line_from_file(file_name="", mode='r'):
    """ function that returns line by line during file reading """
    try:
        file = open(file_name, mode, encoding= 'utf-8')
        for line in file:
            yield line
        file.close()
    except IOError:
        print_err()
        exit(1)

def is_valid_ipmask(ipmask):
    """ check if ipv4/6 and mask are valid """
    try:
        ipaddress.ip_address(ipmask)
        return True
    except ValueError:
        return False

def is_valid_fqdn(fqdn=""):
    """ check if the specified Fully Qualified Domain Name is valid """
    try:
        list_of_netAddresses =  fqdn.split(".")
        length = len(list_of_netAddresses)
        # example.com | www.example.com
        if length == 2 or length == 3:
            return True
        else:
            raise ValueError
    except:
        return False

class Fqdn:
    """ Fully Qualified Domain Name """
    def __init__(self, fqdn):
        if is_valid_fqdn(fqdn):
            self.fqdn = fqdn
        else:
            print("invalid fqdn: "+fqdn+"  ", end="")
            print_err()

class Geography:
    """ Geography-based Address """
    # geography & interface
    def __init__(self, geo, intf):
        self.geo = geo
        self.int = intf

class Wildcard_fqdn:
    pass


class Network:
    """ metaclass: ip and mask or range of ip addresses """
    """ need to add masks like /16 .. """
    def __init__(self, x="", y=""):
        if is_valid_ipmask(x):
            self.x = x
        else:
            print("invalid ip address found: "+ip+"  ",end="")
            print_err()
        if is_valid_ipmask(y):
            self.y = y
        else:
            print("invalid mask found: "+mask+"  ",end="")
            print_err()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Wildcard(Network):
    """  standard IPv4 using a wildcard subnet mask """
    # x : network ip address
    # y : subnet mask
    def __init__(self, ip="", wmask=""):
        Network.__init__(self, ip, wmask)

class Ipmask(Network):
    """ inherit from Network class. Defined as network addr + mask """
    # x : network ip address
    # y : subnet mask
    def __init__(self, x="", y=""):
        Network.__init__(self, x, y)

class Iprange(Network):
    """ inherit from Network class. Defined as a range of ip addresses """
    # x : start ip address
    # y : end ip address
    def __init__(self, x, y):
        Network.__init__(self, x, y)


class Network_addr:
    """ is the name of the network/subnet/host, his type, ip and eventually a comment """
    #all types of addresses
    addrtypes = ['ipmask', 'iprange', 'fqdn', 'geography', 'wildcard', 'wildcard-fqdn']
    comment = ""
    def __init__(self, net_name="", addrtype=""):
        self.net_name = net_name
        if addrtype in self.addrtypes:
            self.addrtype = addrtype

    def set_addr(self, x, y):
        if self.addrtype == 'ipmask':
            self.ip = Ipmask(x, y)
        elif self.addrtype == 'iprange':
            self.ip = Iprange(x, y)

    def set_comment(self, comment=""):
        self.comment = comment

    def get_addr(self):
        return self.ip.get_x(), self.ip.get_y()

    def get_comment(self):
        return self.comment

    def __str__(self):
        return 'name : '+ self.net_name\
            + '\n\t' + self.ip.get_x() + ' ' + self.ip.get_y()\
            + '\n\t' + self.comment

class Address_group:
    """ contain firewall addresses which are the members of this group """
    def __init__(self, group_name=""):
        self.group_name = group_name
        self.members = []

    def add_member(member=""):
        self.members.append(member)

    def get_members():
        return self.members

class File_parser():
    """ parse a configuration file and create needed objects"""
    def __init__(self, file_name=""):
        self.file_name = file_name
        self.list_of_netAddresses = []
        self.conf_addr = False
        self.conf_addrgrp = False
        #name of network address or of the address group
        self.name = ""
        self.addrtype = ""
        self.comment = ""
        # network ip address
        self.x = ""
        # network mask
        self.y = ""

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

    def next_action( self ):
        """ create the correspondent objects with the gathered information
            and store them """
        if self.conf_addr:
            self.net_addr = Network_addr( self.name, self.addrtype )
            self.net_addr.set_addr(self.x, self.y)
            if self.comment != "":
                self.net_addr.set_comment( self.comment )
            # append the newly created network address in the tuple
            self.list_of_netAddresses.append( self.net_addr )

    def end_action( self ):
        """ reinit all attributes"""
        self.addrtype, self.name, self.comment = "", "", ""
        self.x, self.y = "", ""
        self.conf_addr = False
        self.conf_addrgrp = False
        self.list_of_netAddresses = []

    def parse( self ):
        """ read lines from config file and parse information """
        for line in get_line_from_file( self.file_name ):
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

    def get_list_of_netAdresses( self ):
        """ return a list of network address objects """
        return self.list_of_netAddresses

def main():
    if len(sys.argv) < 2:
        print("You should provide a configuration file as an argument as follows:")
        print("\t"+sys.argv[0]+ " config_file.conf")
        exit("\n")

    config_file = sys.argv[1]
    print("Parsing configuration file " + config_file+" ...  ", end="" )

    file_parser = File_parser( config_file )
    file_parser.parse()
    tuple = file_parser.get_list_of_netAdresses()

    [ print(addr) for addr in tuple ]
    print_done()
    csv_file = config_file.split(".")[0]+".csv"
     #print("Creating csv file : " + csv_file )

if __name__ == '__main__':
    main()
