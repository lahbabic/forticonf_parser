#-*- coding: utf-8 -*

import json

class Object:

    def __init__( self, tmp_dict=None ):
        """ set all object attributes """
        if tmp_dict is None:
            tmp_dict = {}
        keys = tmp_dict.keys()
        # for each key in the dictionary keys
        for key in keys:
            attr = key
            # if the key contain '-'
            if "-" in key:
                # change it to '_'
                # because attributes can't have '-' in their names
                attr = key.replace( "-", "_" )
            # if the object has this attribute
            if hasattr( self, attr ):
                # set his attribute with the corresponding value
                setattr( self, attr, tmp_dict[ key ] )

    def __str__( self ):
        """ create a printable representation of this object """
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

    def get_attrs( self ):
        """
            return all attributes in a dictionary
        """
        tmp = {}
        # for key in the object implemented attributes
        for key in self.implemented_keys:
            # check if the object has the attribute 'key'
            if hasattr( self, key ):
                # if so, get the attribute value and store it into the tmp
                # dictionary with the corresponding key
                tmp[ key ] = getattr( self, key )
                # if the attribute value is None
                if not tmp[ key ]:
                    tmp[ key ] = ""
        return json.dumps( tmp, indent=4 )

    def convert_to_row( self ):
        """ return a list containing all attributes """
        row = []
        keys = self.implemented_keys
        # add the 'member_of' key to get the groups that the object belong to
        if self.__class__.__name__ == "Network_addr":
            # generator that create a new list from the object implemented_keys
            # list without the "type" key
            keys = [ key for key in self.implemented_keys if key != "type" ]

        for key in keys:
            if hasattr( self, key ):
                value = getattr( self, key )
                # if value is not a list
                if not isinstance( value, list ):
                    row.append( value )
                # if value is a list
                elif key == 'ip':
                    for x in value:
                        row.append( x )
                else:
                    row.append( ' '.join( value ) )
        return row

    def convert_to_json( self ):
        pass
