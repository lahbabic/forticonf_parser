#-*- coding: utf-8 -*

""" policies are essentially discrete compartmentalized sets of instructions
    that control the traffic flow going through the firewall.
    These instructions control where the traffic goes, how it’s processed,
    if it’s processed and even whether or not it’s allowed to pass through the FortiGate."""


class Policy:

    implemented_fields = ['policy_number', 'srcintf', 'dstintf', 'srcaddr',\
                'dstaddr', 'action', 'schedule', 'service', 'logtraffic',\
                'global_label', 'nat', 'status', 'comments']

    def __init__(self, tmp_dict={}):
        self.policy_number = ""
        self.srcintf = []
        self.dstintf = []
        self.srcaddr = ""
        self.dstaddr = ""
        self.action = ""
        self.schedule = ""
        self.service = []
        self.logtraffic = ""
        self.global_label = ""
        self.nat = ""
        self.status = ""
        self.comments = ""

        keys = tmp_dict.keys()
        for key in keys:
            attr = key
            if "-" in key:
                attr = key.replace("-", "_")
            if attr in self.implemented_fields:
                setattr(self, attr, tmp_dict[ key ])

    def get_attrs( self ):
        """
            return all attribute in a dictionary
        """
        tmp = {}
        for key in self.implemented_fields:
            tmp[ key ] = getattr(self, key)
            if not tmp[ key ]:
                tmp[ key ] = ""
        return tmp

    def __str__( self ):
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
