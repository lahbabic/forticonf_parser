#-*- coding: utf-8 -*


class Service:
    """ contain a list of used protocols and ports """

    implemented_keys = ['name', 'explicit_proxy', 'protocol', 'protocol_number',\
               'visibility', 'icmptype', 'icmpcode', 'tcp_portrange', 'udp_portrange'\
               'sctp_portrange']

    def __init__( self, dict={} ):
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
        # get all keys in dict, wich mean that this keys have defined values
        keys = dict.keys()
        for key in keys:
            attr = key
            if "-" in key:
                attr = key.replace("-", "_")
            if attr in self.implemented_keys:
                setattr(self, attr, dict[ key ])

    def __str__( self ):
        """ create a printable representation of this object"""
        ret = ""
        for key in self.implemented_keys:
            if hasattr(self, key):
                value = getattr(self, key)
                # if value is not None and is not a list
                if value and not isinstance(value, list):
                    ret += str(key)+': '+str(value)+'\n'
                # if value is not None and is a list
                elif value and isinstance(value, list):
                    ret += str(key)+': '
                    for x in value:
                        ret += str(x)+' '
                    ret += '\n'
        return ret

    def get_name( self ):
        return self.name

    def get_attrs( self ):
        """
            return all attribute in a dictionary
        """

class Service_group:
    """ Group containing a list of services """

    def __init__( self, name="" ):
        self.name = name
        self.services = []

    def add_service(self, member="" ):
        self.services.append( member )

    def get_services( self ):
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
