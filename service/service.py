#-*- coding: utf-8 -*


class Service:
    """ contain a list of used protocols and ports """

    implemented_keys = ['name', 'explicit_proxy', 'protocol', 'protocol_number',\
               'visibility', 'icmptype', 'icmpcode', 'tcp_portrange', 'udp_portrange']

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
        ''' '''
        self.sctp_portrange = []
        ''' visibility to include this service in firewall policy service selection '''
        self.visibility = ""
        self.comment = ""
        # get all keys in dict, wich mean that this keys have defined values
        keys = dict.keys()
        for key in keys:
            if key in self.implemented_keys:
                attr = key
                if "-" in key:
                    attr = key.replace("-", "_")
                setattr(self, attr, dict[ key ])

    def get_fields( self ):
        pass

    def __str__( self ):
        """ create a printable representation of this object"""
        ret = ""
        for key in self.implemented_keys:
            value = getattr(self, key)
            # if value is not None and is a list
            if value and not isinstance(value, list):
                ret += str(key)+': '+str(value)+'\n'
            # if value is not None and is a list
            else:
                ret += str(key)+': '
                for x in value:
                    ret += str(x)+' '
                ret += '\n'
        return ret

    def get_name( self ):
        return self.name


class ServiceGrp:
    pass
