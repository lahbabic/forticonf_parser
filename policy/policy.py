#-*- coding: utf-8 -*

""" policies are essentially discrete compartmentalized sets of instructions
    that control the traffic flow going through the firewall.
    These instructions control where the traffic goes, how it’s processed,
    if it’s processed and even whether or not it’s allowed to pass through the FortiGate."""


class Policy:

    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.srcintf = []
        self.dstintf = []
        self.srcaddr = ""
        self.dstaddr = ""
        self.action = ""
        self.schedule = ""
        self.services = []
        self.logtraffic = ""

    def set_src_dst_intf( src="", dst="" ):
        self.srcintf = src
        self.dstintf = dst

    def set_src_dst_addr( src="", dst="" ):
        self.srcaddr = src
        self.dstaddr = dst

    def set_action( action="" ):
        self.action = action

    def set_schedule( schedule="" ):
        self.schedule = schedule

    def add_service( service="" ):
        self.services.append( service )

    def set_logtraffic( logtraffic="" ):
        self.logtraffic = logtraffic

    def __str__():
        return 'policy : ' + self.policy_number + '\n\tsrcintf: ' +
                self.srcintf + '\n\tdstintf: '+ self.dstintf
                + '\n\tsrcaddr: ' + self.srcaddr + '\n\tdstaddr: '
                + '\n\taction: ' + self.action + '\n\tschedule: '
                + '\n\tservices' + ' '.join( self.services )
