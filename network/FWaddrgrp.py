#-*- coding: utf-8 -*
class Address_group:
    """ contain firewall addresses which are the members of this group """
    def __init__(self, group_name=""):
        self.group_name = group_name
        self.members = []

    def add_member(self, member=None):
        self.members.append(member)

    def get_name( self ):
        return self.group_name

    def get_members( self ):
        return self.members

    def __str__( self ):
        return 'name : '+ self.group_name +"\n"+\
                'members:' + ' '.join( self.members )
