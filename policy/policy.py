#-*- coding: utf-8 -*

from object import *
from print_x import *

""" policies are essentially discrete compartmentalized sets of instructions
    that control the traffic flow going through the firewall.
    These instructions control where the traffic goes, how it’s processed,
    if it’s processed and even whether or not it’s allowed to pass through the FortiGate."""

""" inherite from the 'Object' class """
class Policy(Object):

    implemented_keys = ['policy_number', 'srcintf', 'dstintf', 'srcaddr',\
                'dstaddr', 'action', 'schedule', 'service', 'logtraffic',\
                'global_label', 'nat', 'status', 'comments', 'ippool', 'poolname']

    def __init__(self, tmp_dict={}):
        self.policy_number = 0
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
        self.ippool = ""
        self.poolname = ""

        super().__init__( tmp_dict )

    def get_id( self ):
        return self.policy_number
