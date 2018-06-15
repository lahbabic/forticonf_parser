#-*- coding: utf-8 -*



class Object:

    def __init__( self, dict={} ):
        """ set all object attributes """
        keys = dict.keys()
        for key in keys:
            attr = key
            if "-" in key:
                attr = key.replace( "-", "_" )
            if hasattr( self, attr ):
                setattr( self, attr, dict[ key ] )

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
            return all attribute in a dictionary
        """
        tmp = {}
        for key in self.implemented_keys:
            tmp[ key ] = getattr(self, key)
            if not tmp[ key ]:
                tmp[ key ] = ""
        return tmp

    def convert_to_row( self , group="" ):
        """ return a list containing all attributes """
        row = []
        keys = self.implemented_keys
        if group:
            row.append( group )

        if self.__class__.__name__ == "Network_addr":
            keys = [ key for key in self.implemented_keys if key != "type" ]

        for key in keys:
            if hasattr( self, key ):
                value = getattr( self, key )
                # if value is not a list
                if not isinstance(value, list):
                    row.append( value )
                # if value is a list
                else:
                    if self.__class__.__name__ == "Network_addr":
                        for x in value:
                            row.append( x )
                    else:
                        row.append( ' '.join( value ) )
        return row
