#-*- coding: utf-8 -*

from host.FWaddress import *
from service.service import *
from policy.policy import *
from print_x import *


class File_reader():
    """
        read lines from file, return lines until 'end' keyword
        if action is : 'config firewall object'
        object can be [address, addrgrp, policy, service, servicegrp]
    """
    def __init__( self, file_name="" ):
        self.file_name = file_name

    def get_line_from_file( self ):
        """ function that returns line by line during file reading """
        try:
            # open the file
            file = open( str(self.file_name), 'r', encoding='utf-8')
            # for each line in the file
            for line in file:
                # yield (return) the line
                yield line
            # when we finish form reading the file, close it
            file.close()
        except :
            print_err()
            print("Failed to process file \n")
            exit(1)


    def get_objects( self, object='' ):
        """
            return a list containing all objects after 'config firewall object'
            if object in [address, addrgrp, policy, service, servicegrp]
        """
        # if the object sought is not in this list (list of processed object)
        # then return none
        if object not in ['address', 'addrgrp', 'policy', 'service custom', 'service group']:
            print_warning()
            print("Can't parse the object "+B+object+W+" from the file, not implemented yet")
            return None
        # set to True if 'object' is found
        object_found = False
        lines, service = [], []
        action = ""

        if 'service' in object:
            service = object.split()

        for line in self.get_line_from_file():
            try:
                # get the action (config, set, unset ...) and it's arguments
                action, *args = line.split()
            except:
                pass
            if action == 'end':
                object_found = False
            elif action == 'config' and args[0] == 'firewall':
                # if the corresponding object is found
                if len(service) == 2\
                        and service[0] and service[1] in args\
                        or object in args:
                    object_found = True

            if object_found == True:
                lines.append( line.strip("\n").strip() )
        print_done()
        return lines


class File_parser():
    """ parse a configuration file and create needed objects """

    def __init__( self, file_name="" ):
        self.file_reader = File_reader( file_name )
        # list containing Network_addr objects
        self.list_of_netAddresses = []
        # list containing Address_grsoup objects
        self.list_of_addrGrp = []
        # list containing the members of a group
        self.list_of_members = []
        # list containing service custom objects
        self.list_of_services = []
        # list containing service group objects
        self.list_of_srvGrp = []
        # list containing policy objects
        self.list_of_policies = []
        # list containing tuples of hosts and a list of groups they belong to
        self.tuples_h_gs = []

    def groups_containing_obj(self, obj_type="", obj_name=""):
        """ returns all groups in which the specific object is located """

        if obj_type == "host":
            list_of_objects = self.list_of_addrGrp
        elif obj_type == "service":
            list_of_objects = self.list_of_srvGrp

        return ' '.join([ group.get_name() for group in list_of_objects
            if obj_name in group.get_members() ])

    def create_addrgrpObj(self, lines=[]):
        """ create 'firewall addrgrp' objects """
        if not lines:
            return None

        command, name, comment = "", "", ""
        args, addrgrp_list = [], []

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                name = args[0].strip('"')
            elif command == 'set':
                if args[0] == "member":
                    # pop 'member' keyword
                    args.pop(0)
                    [ addrgrp_list.append( member ) for member in args ]
                elif args[0] == "comment":
                    # pop 'comment' keyword
                    args.pop(0)
                    comment = ' '.join(args).strip('"')
            elif command == "next":
                addr_grp = Address_group( name )
                [ addr_grp.add_member(member.strip('"')) for member in addrgrp_list ]
                addr_grp.set_comment( comment )
                self.list_of_addrGrp.append( addr_grp )
                # reinit variables
                command, name, comment = "", "", ""
                args, addrgrp_list = [], []
        print_done()

    def create_addrObj(self, lines=[]):
        """
            create network address objects from lines
            'firewall address'
        """
        if not lines:
            return None

        implemented_commands = ['config', 'edit', 'set', 'next']
        unimplemented_commands = []

        net_addr = {}
        x, y = "", ""
        command = ""
        args = []

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                net_addr['name'] = args[0].strip('"')
                net_addr['member_of'] = \
                            self.groups_containing_obj("host", net_addr['name'])
            elif command == 'set':
                if args[0] == 'subnet':
                    net_addr['type'] = 'ipmask'
                    x, y = args[1], args[2]
                elif args[0] == 'type' and args[1] == 'ipmask':
                    net_addr['type'] = 'ipmask'
                elif args[0] == 'type' and args[1] == 'iprange':
                    net_addr['type'] = 'iprange'
                elif args[0] == 'start-ip':
                    x = args[1]
                elif args[0] == 'end-ip':
                    y = args[1]
                elif args[0] == 'comment':
                    # pop the 'comment' keyword
                    args.pop(0)
                    net_addr['comment'] = ' '.join(args)
            elif command == 'next':
                if net_addr.get('type'):
                    net_addr['ip'] = []
                    net_addr['ip'].append(x)
                    net_addr['ip'].append(y)
                    addr = Network_addr( net_addr )
                    self.list_of_netAddresses.append(addr)
                    x, y = "", ""
                    net_addr.clear()
            if command not in implemented_commands:
                if command not in unimplemented_commands:
                    print_warning()
                    print(B+command+W+" command not implemented yet")
                    unimplemented_commands.append( command )
        print_done()

    def create_serviceCObj(self, lines=[]):
        """ create 'firewall service custom' objects """
        if not lines:
            return None

        command = ""
        args, service_list = [], []
        service = {}
        implemented_commands = ['config', 'edit', 'set', 'next']
        unimplemented_fields = []
        unimplemented_commands = []
        implemented_fields = ['service_name', 'explicit-proxy', 'protocol', 'protocol-number',
                   'visibility', 'icmptype', 'icmpcode', 'category', 'comment']

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                service['service_name'] = args[0].strip('"')
                service['member_of'] = \
                            self.groups_containing_obj("service", service['service_name'])
            elif command == 'set':
                try:
                    # This 3 fields can contain multiple entries
                    if args[0] == 'tcp-portrange' or args[0] == 'udp-portrange' or\
                    args[0] == 'sctp-portrange':
                        portrange_type = args[0]
                        args.pop(0)
                        service[ portrange_type ] = ' '.join(args)
                    elif args[0] in implemented_fields:
                        service[ args[0] ] = args[1]
                    elif args[0] not in implemented_fields:
                        if args[0] not in unimplemented_fields:
                            print_warning()
                            print("Can't set the field "+B+args[0]+W+", not implemented yet")
                            unimplemented_fields.append( args[0] )
                except:
                    pass
            elif command == 'unset':
                pass
            elif command == 'next':
                service_Obj = Service( service )
                self.list_of_services.append( service_Obj )
                portrange_type = ""
                service.clear()
            if command not in implemented_commands:
                if command not in unimplemented_commands:
                    print_warning()
                    print(B+command+W+" command not implemented yet")
                    unimplemented_commands.append( command )
        print_done()

    def create_serviceGObj(self, lines=[]):
        """ create 'service group' objects """
        if not lines:
            return None

        command, name = "", ""
        args, serv_list = [], []

        for line in lines:
            try:
                command, *args = line.split()
            except:
                pass

            if command == 'edit':
                name = args[0].strip('"')
            elif command == 'set':
                if args[0] == "member":
                    # pop 'member' keyword
                    args.pop(0)
                    [ serv_list.append( member ) for member in args ]
            elif command == "next":
                srv_grp = Service_group( name )
                [ srv_grp.add_service(service.strip('"')) for service in serv_list ]
                self.list_of_srvGrp.append( srv_grp )
                # reinit variables
                command, name = "", ""
                args, serv_list = [], []
        print_done()

    def get_policy_id(self, policy):
        """ return the id of the policy, used for sorting """
        return policy.get_id()

    def create_policyObj(self, lines=[]):
        """ create 'policy' objects """
        if not lines:
            return None

        implemented_commands = ['config', 'edit', 'set', 'next']
        unimplemented_commands = []
        implemented_fields = ['policy_number', 'srcintf', 'dstintf', 'srcaddr',\
                    'dstaddr', 'action', 'schedule', 'service', 'logtraffic',\
                    'global-label', 'nat', 'status', 'comments', 'ippool', 'poolname']
        unimplemented_fields = []
        policy = {}
        command = ""
        args = []
        for line in lines:
            if not line:
                pass
            try:
                command, *args = line.split()
            except:
                pass
            if command == 'edit':
                try:
                    policy['policy_number'] = int(args[0].strip('"'))
                except:
                    print('not a valid id:' + policy['policy_number'])
            elif command == 'set':
                # the field must be in implemented_fields
                field = args.pop(0)
                if field in implemented_fields:
                    # if the field value is a list
                    if isinstance(args, list):
                        policy[ field ] = '  '.join( args ).replace('"', '')
                    else:
                        policy[ field ] = args.strip('"')
                elif field not in implemented_fields:
                    if field not in unimplemented_fields:
                        print_warning()
                        print("Can't set the field "+B+field+W+", not implemented yet")
                        unimplemented_fields.append( field )
            elif command == 'next':
                policy_obj = Policy( policy )
                if self.get_policy_id(policy_obj) != 0:
                    self.list_of_policies.append(policy_obj)
                policy.clear()
        # sort policies by id
        try:
            self.list_of_policies = sorted( self.list_of_policies, key=self.get_policy_id )
        except:
            print_warning()
            print("Can't sort policies")
        print_done()

    def parse(self, object_to_look_for=""):
        """
            get lines from file that match the object specified
            in argument to search for, and create the corresponding objects
        """
        if object_to_look_for == "":
            """ fetch all objects """
            self.parse("hosts")
            self.parse("services")
            self.parse("policies")

        elif object_to_look_for == "hosts":
            print("File parsing for"+B+" addrgrp"+W+" objects ...  ", end="" )
            addrgrp_lines = self.file_reader.get_objects( 'addrgrp' )
            if not addrgrp_lines:
                print("Their is no address group objects")
            else:
                print("Creating addrgrp objects ...  ", end="" )
                self.create_addrgrpObj( addrgrp_lines )

            print("File parsing for"+B+" address"+W+" objects ...  ", end="" )
            addrs_lines = self.file_reader.get_objects( 'address' )
            if not addrs_lines:
                print("Their is no address objects")
            else:
                print("Creating address objects ...  ", end="" )
                self.create_addrObj( addrs_lines )

        elif object_to_look_for == "services":
            print("File parsing for"+B+" service group"+W+" objects ...  ", end="" )
            serviceGrp_lines = self.file_reader.get_objects( 'service group' )
            if not serviceGrp_lines:
                print("Their is no service group objects")
            else:
                print("Creating service group objects ...  ", end="" )
                self.create_serviceGObj( serviceGrp_lines )

            print("File parsing for"+B+" service custom"+W+" objects ...  ", end="" )
            serviceC_lines = self.file_reader.get_objects( 'service custom' )
            if not serviceGrp_lines:
                print("Their is no service custom objects")
            else:
                print("Creating service custom objects ...  ", end="" )
                self.create_serviceCObj( serviceC_lines )

        elif object_to_look_for == "policies":
            print("File parsing for"+B+" policy"+W+" objects ...  ", end="" )
            policies_lines = self.file_reader.get_objects( 'policy' )
            if not policies_lines:
                print("Their is no policy objects")
            else:
                print("Creating policy objects ...  ", end="" )
                self.create_policyObj( policies_lines )

    def get_addrgrp_byName(self, name=""):
        """ return addrgrp object that has the name given in argument """
        for addrgrp in self.list_of_addrGrp:
            if addrgrp.get_name() == name:
                return addrgrp
        return None

    def get_serviceGrp_byName(self, name=""):
        """ return service group object that has the name given in argument """
        for serviceG in self.list_of_srvGrp:
            if serviceG.get_name() == name:
                return serviceG
        return None

    def get_obj_byName(self, type="", name=""):
        """ return object that has the name and the type given in argument """
        if type == "hosts":
            for net_addr in self.list_of_netAddresses:
                if net_addr.get_name() == name:
                    return net_addr
            return None
        elif type == "services":
            for service in self.list_of_services:
                if service.get_name() == name:
                    return service
            return None

    def get_list_of_netAdresses(self):
        """ return a list of network address objects """
        return self.list_of_netAddresses

    def get_list_of_addrGrp(self):
        """ return a list of address group objects """
        return self.list_of_addrGrp

    def get_list_of_Cservices(self):
        """ return a list of service custom objects """
        return self.list_of_services

    def get_list_of_Gservices(self):
        """ return a list of service Group objects """
        return self.list_of_srvGrp

    def get_list_of_policies(self):
        """ return a list of policy objects """
        return self.list_of_policies
