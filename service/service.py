#-*- coding: utf-8 -*

from object import *

class Service(Object):
    """ contain a list of used protocols and ports """

    implemented_keys = ['service_name', 'tcp_portrange', 'udp_portrange',\
    'sctp_portrange', 'explicit_proxy', 'protocol', 'protocol_number',\
               'visibility', 'icmptype', 'icmpcode', 'category', 'comment']

    def __init__( self, tmp_dict={} ):
        self.service_name = ""
        ''' configure this service as an explicit web proxy service,
            The service will be available to explicit proxy firewall
            policies but not to regular firewall policies. '''
        self.explicit_proxy = ""
        ''' Assign the service to a service category '''
        self.category = ""
        ''' Protocol used by the service '''
        self.protocol = ""
        ''' IP address or address range for this service '''
        self.iprange = ""
        ''' For an IP service, enter the IP protocol number '''
        self.protocol_number = ""
        ''' ICMP type number. The range for type_int is from 0-255 '''
        self.icmptype = ""
        ''' ICMP code number '''
        self.icmpcode = ""
        '''
            example:
            set tcp-portrange 100-150:1100-1150 2000-2100:4000-4100
        '''
        self.tcp_portrange = []
        '''
            UDP services, the destination and source port ranges.
        '''
        self.udp_portrange = []
        self.sctp_portrange = []
        ''' visibility to include this service in firewall policy service selection '''
        self.visibility = ""
        self.category = ""
        self.comment = ""

        super().__init__( tmp_dict )




    def get_name( self ):
        return self.service_name


class Service_group:
    """ Group containing a list of services """

    def __init__( self, name="" ):
        self.name = name
        self.services = []

    def add_service(self, member="" ):
        self.services.append( member )

    def get_members( self ):
        return self.services

    def get_name( self ):
        return self.name

    def __str__( self ):
        ret = "name: " + self.name + "\n"
        ret += "services: "
        for service in self.services:
            ret += service + " "
        ret += "\n"
        return ret
