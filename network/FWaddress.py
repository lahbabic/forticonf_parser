#-*- coding: utf-8 -*
import ipaddress

""" firewall addresses used in firewall policies.
    An IPv4 firewall address is a set of one or more IP addresses,
    represented as a domain name, an IP address and a subnet mask,
    or an IP address range. An IPv6 firewall address is an IPv6 address prefix
    source: http://help.fortinet.com/cli/fos50hlp/54/Content/FortiOS/fortiOS-cli-ref-54/config/firewall/address.htm """

W = '\033[0m'   # white
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m'  # blue

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
        self.addrtype = None
        if addrtype in self.addrtypes:
            self.addrtype = addrtype
        else:
            print("Address type "+B +addrtype+ W+" not implemented yet")


    def set_addr(self, x, y):
        if self.addrtype == 'ipmask':
            self.ip = Ipmask(x, y)
        elif self.addrtype == 'iprange':
            self.ip = Iprange(x, y)
        else:
            pass

    def get_name(self):
        return self.net_name

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
