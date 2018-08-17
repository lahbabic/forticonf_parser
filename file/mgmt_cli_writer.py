 #-*- coding: utf-8 -*

from print_x import *

class Mgmt_cli_writer:

    def __init__(self, parser=None, file_name=""):
        self.parser = parser
        self.file_name = file_name
        self.created_hosts = []

    def check_if_host(self, ip_mask=""):
        " Return True if the address is a host"
        if ip_mask is None:
            return None
        if ip_mask[1] == "255.255.255.255":
            return "host"
        else:
            return "net"


    def get_objects(self, objects="", type="", tmp=[]):
        " Return a list of addresses or services by retrieving their name"
        if objects is None:
            return tmp

        for obj_name in objects:
            obj = self.parser.get_obj_byName(type, obj_name)
            if obj is None:
                grp = None
                if type == "hosts":
                    grp = self.parser.get_addrgrp_byName(obj_name)
                elif type == "services":
                    grp = self.parser.get_serviceGrp_byName(obj_name)
                if grp is None:
                    return tmp
                return self.get_objects(grp.get_members(), type, tmp)
            tmp.append(obj)
        return tmp


    def addr_to_mgmt_cli(self, addr=""):
        if not addr:
            return None
        is_host = self.check_if_host( addr.ip )

        addr = addr.get_attrs()
        if addr['name'] in self.created_hosts:
            return None

        command = 'mgmt_cli add '
        if is_host == "host":
            command += 'host name'
            command += ' "'+ addr["name"] +'"'
            command += ' ip-address "'+ addr["ip"][0] + '"'
            command += ' '
        elif is_host == "net":
            command += 'network name'
            command += ' "'+ addr["name"] +'"'
            command += ' subnet "'+ addr["ip"][0] + '"'
            command += ' subnet-mask "'+ addr["ip"][1] + '"'

        self.created_hosts.append(addr['name'] )
        return command


    def policy_to_mgmt_cli(self, policy=""):

        src_addresses = policy["srcaddr"].split()
        dst_addresses = policy["dstaddr"].split()
        services = policy["service"].split()
        print(policy["policy_number"])
        #get host or services names if their is a group get his members
        src_addrs = self.get_objects( src_addresses, "hosts", [] )
        dst_addrs = self.get_objects( dst_addresses, "hosts", [] )
        srvs = self.get_objects( services, "services", [] )

        [ print(addr.get_name()) for addr in dst_addrs ]
        print("\n_________________________\n")
        p = "add access-rule layer network position bottom "
        p += "action " + policy["action"] + " "
        p += "destination " + " ".join([ addr.get_name() for addr in dst_addrs ])
        p += " source " + " ".join([ addr.get_name() for addr in src_addrs ])
        p += " service " + " ".join([srv.get_name() for srv in srvs ])

        for addr in src_addrs + dst_addrs:
            command = self.addr_to_mgmt_cli(addr)
            if command is not None:
                yield command
        yield p

    def write_specific_policies(self):
        try:
            # open the file
            file = open( str(self.file_name), 'w+', encoding='utf-8')

            for cmd in self.spec_policies_to_mgmt_cli():
                file.write(cmd)
                file.write("\n")

            file.close()
        except :
            print_err()
            print("Failed to process file \n")
            exit(1)




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
