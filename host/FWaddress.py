#-*- coding: utf-8 -*
from ipaddress import ip_address
from object import *
from print_x import *

""" firewall addresses used in firewall policies.
    An IPv4 firewall address is a set of one or more IP addresses,
    represented as a domain name, an IP address and a subnet mask,
    or an IP address range. An IPv6 firewall address is an IPv6 address prefix
    source: http://help.fortinet.com/cli/fos50hlp/54/Content/FortiOS/fortiOS-cli-ref-54/config/firewall/address.htm """



def is_valid_ipmask(ipmask):
    """ check if ipv4/6 and mask are valid """
    try:
        ip_address(ipmask)
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

""" inherite from the 'Object' class """
class Network_addr(Object):
    """ is the name of the network/subnet/host, his type, ip and eventually a comment """

    implemented_types = ['ipmask', 'iprange']
    unimplemented_types = ['fqdn', 'geography', 'wildcard', 'wildcard-fqdn']
    implemented_keys = ['name', 'type', 'ip', 'comment']

    def __init__( self, tmp_dict={} ):
        self.name = ""
        self.type = ""
        ''' tuple containing ip/mask or iprange for now '''
        self.ip = None
        self.comment = ""

        keys = tmp_dict.keys()
        if not is_valid_ipmask(tmp_dict['ip'][0]) or not is_valid_ipmask(tmp_dict['ip'][1]):
            print_warning()
            print("Invalid ip/mask "+B+tmp_dict['ip'][0]+" "+tmp_dict['ip'][1]+W)

        super().__init__( tmp_dict )

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.ip[0], self.ip[1]

    def get_comment(self):
        return self.comment



class Address_group:
    """ contain firewall addresses which are the members of this group """
    def __init__( self, group_name="" ):
        self.group_name = group_name
        # members is a list of str objects
        self.members = []
        self.comment = ""

    def add_member( self, member=None ):
        self.members.append( member )

    def set_comment( self, comment="" ):
        self.comment = comment

    def get_name( self ):
        return self.group_name

    def get_members( self ):
        return self.members

    def __str__( self ):
        if self.comment == "":
            return 'name: '+ self.group_name +"\n"+\
                    'members:' + ' '.join( self.members ) + "\n"
        else:
            return 'name: '+ self.group_name +"\n"+\
                    'members: ' + ' '.join( self.members ) +"\n"+\
                    'comment: ' + self.comment + "\n"
