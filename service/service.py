#-*- coding: utf-8 -*


class service:
    """ contain a list of used protocols and ports """

    def __init__( self, name="" ):
        self.name = name
        self.proto_port = []

    def add_protocol_port( self, protocol="", port="" ):
        self.proto_port.append( {'Protocol': protocol, 'Port': port } )

    def get_name( self ):
        return self.name

    def get_proto_ports( self ):
        return self.proto_port

    def __str__( self ):
        ret = 'name:' + self.name + "\n"
        for x in self.proto_port:
            ret += str(x)
        return ret
