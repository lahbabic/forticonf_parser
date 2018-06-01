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


def is_valid_fqdn(fqdn=""):
    """ check if the specified Fully Qualified Domain Name is valid """
    try:
        tmp =  fqdn.split(".")
        length = len(tmp)
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

def is_valid_ipmask(ipmask):
    """ check if ipv4/6 and mask are valid """
    try:
        ipaddress.ip_address(ipmask)
        return True
    except ValueError:
        return False

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

    def get_x():
        return self.x

    def get_y():
        return self.y

class Wildcard(Network):
    """  standard IPv4 using a wildcard subnet mask """
    # x : network ip address
    # y : subnet mask
    def __init__(self, ip="", wmask=""):
        Network.__init__(self, ip, wmask)

class Ipmask(Network):
    """ inherit from Network class. network addr + mask """
    # x : network ip address
    # y : subnet mask
    def __init__(self, x="", y=""):
        Network.__init__(self, x, y)

class Iprange(Network):
    """ inherit from Network class. a range of ip addresses """
    # x : start ip address
    # y : end ip address
    def __init__(self, x, y):
        Network.__init__(self, x, y)


class Network_addr:
    """ config firewall address(es) """
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
        if self.addrtype == 'ipmask':
            return ipmask.get_subnet(), ipmask.get_mask()
        elif self.addrtype == 'iprange':
            return iprange

    def get_comment(self):
        return self.comment

    def __str__(self):
        return 'name : '+ self.net_name


class Address_group:
    """ contain firewall addresses which are the members of this group """
    def __init__(self, group_name=""):
        self.group_name = group_name
        self.members = []

    def add_member(member=""):
        self.members.append(member)

    def get_members():
        return self.members

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

def parse_file(file_name=""):
    conf = {}
    tmp = []
    conf_addr = False
    conf_addrgrp = False
    #name of network address or of the address group
    name = ""
    addrtype = ""
    # network ip address
    x = ""
    # network mask
    y = ""
    for line in get_line_from_file(file_name):
        try:
            action, *args = line.split()
        except:
            pass

        """ raffiner cette fonction """
        if action == 'config':
            if args[-1] == 'address':
                conf_addr = True
            elif args[-1] == 'addrgrp':
                conf_addrgrp = True
        elif action == 'edit':
            name = ' '.join(args).strip('"')
        elif action == 'set':
            if conf_addr:
                if args[0] == 'subnet':
                    addrtype = 'ipmask'
                    # network ip address
                    x = args[1]
                    # network mask
                    y = args[2]
                elif args[0] == 'type':
                    if args[1] == 'ipmask':
                        addrtype = args[1]
                    elif args[1] == 'iprange':
                        addrtype = args[1]
                elif args[0] == 'start-ip':
                    x = args[1]
                elif args[0] == 'end-ip':
                    y = args[1]
        elif action == 'next':
            if conf_addr:
                net_addr = Network_addr(name, addrtype)
                net_addr.set_addr(x, y)
                tmp.append( net_addr )
        elif action == 'end':
            addrtype = ""
            name = ""
            conf_addr = False
            conf_addrgrp = False
            x, y = "", ""
        """ajouter elif comment"""
    [ print(obj) for obj in tmp]
    return tmp

def main():
    if len(sys.argv) < 2:
        print("You should provide a configuration file in argument as follows:")
        print("\t"+sys.argv[0]+ " config_file.conf")
        exit("\n")

    config_file = sys.argv[1]
    print("Parsing configuration file " + config_file+" ...  ", end="" )

    conf = parse_file( config_file )
    print_done()
    csv_file = config_file.split(".")[0]+".csv"
    print("Creating csv file : " + csv_file )

    write_to_csv(conf, csv_file)
    print("done")

    net_addr = Network_addr("h-fr-sel", 'ipmask')
    net_addr.set_addr("192.168.1.1", "255.255.255.255")
    print( net_addr.get_addr() )

if __name__ == '__main__':
    main()
