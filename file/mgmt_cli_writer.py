#-*- coding: utf-8 -*

class Mgmt_cli_writer:

    def __init__(self, parser=None, file_name=""):
        self.parser = parser
        self.file_name = ""
        attrs_to_mgmt_cli = {
            "" : "",
            "" : ""
        }

    def check_if_host(self, ip_mask=""):
        " Return True if the address is a host"
        if ip_mask is None:
            return False
        if ip_mask[1] == "255.255.255.255":
            return True
        else:
            return False

    def get_addresses(self, addresses="", tmp=[]):
        if addresses is None:
            return tmp

        for addr in addresses:
            addr_obj = self.parser.get_obj_byName("hosts", addr)
            if addr_obj is None:
                addr_grp_obj = self.parser.get_addrgrp_byName(addr)
                if addr_grp_obj is None:
                    return None
                return self.get_addresses(addr_grp_obj.get_members(), tmp)
            tmp.append( addr_obj )
        return tmp

    def addr_to_mgmt_cli(self, addr=""):
        if not addr:
            return None
        is_host = self.check_if_host( addr.ip )

        command = 'mgmt_cli add '
        if is_host:
            command += 'host name'
            addr = addr.get_attrs()
            command += ' "'+ addr["name"] +'"'
            command += ' ip-address "'+ addr["ip"][0] + '"'
            command += ' '
        else:
            command += 'network name'
            addr = addr.get_attrs()
            command += ' "'+ addr["name"] +'"'
            command += ' subnet "'+ addr["ip"][0] + '"'
            command += ' subnet-mask "'+ addr["ip"][1] + '"'
        return command


    def policy_to_mgmt_cli(self, policy=""):
        """
        """
        src_addresses = policy["srcaddr"].split()
        dst_addresses = policy["dstaddr"].split()
        #convert this names into ip addresses
        src_addrs = self.get_addresses( src_addresses )
        dst_addrs = self.get_addresses( dst_addresses )
        try:
            print(src_addrs)
            print(dst_addrs)
            print(len(src_addrs)+len(dst_addrs))
            print(len(src_addrs + dst_addrs))
        except:
            print(policy)
        for addr in src_addrs + dst_addrs:
            command = self.addr_to_mgmt_cli(addr)
            yield addr


    def write_specific_policies(self):

        for cmd in self.spec_policies_to_mgmt_cli():
            print(cmd)



    def spec_policies_to_mgmt_cli(self):
        """ return a list containing mgmt_cli commands to create
            specific policies, if policies
            contains objects it create this objects
        """
        policies = self.parser.get_list_of_policies()
        if policies is None:
            return 1

        mgmt_cli_commands = []
        tmp_addresses = []
        # Generator that create a list of specific policies
        # specific policies are policies that have their id lower than 100
        specific_policies = [ policy for policy in policies\
                            if policy.get_id() <= 100 ]

        for policy in specific_policies:
            #get policy attributes and values in dictionary
            policy_dict = policy.get_attrs()

            for command in self.policy_to_mgmt_cli( policy_dict ):
                yield command

            """#get source addresses (names)
            src_addresses = policy_dict["srcaddr"].split()
            #convert this names into ip addresses
            tmp_addresses = self.get_addresses( src_addresses )
            #check if the address is a host or is a network
            #and create it's mgmt_cli command
            for addr in tmp_addresses:
                mgmt_cli_command = ""
                mgmt_cli_command = self.convert_to_mgmt_cli( "addr", addr )
                #if the command is not None
                if mgmt_cli_command:
                    yield mgmt_cli_command

            mgmt_cli_command = ""
            mgmt_cli_command = self.convert_to_mgmt_cli( "policy", policy_dict )
            if mgmt_cli_command:
                yield mgmt_cli_command
            exit()
        """
        """
            Need to convert policies
        """
