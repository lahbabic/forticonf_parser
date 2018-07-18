#-*- coding: utf-8 -*

import requests, json
import inspect

"""
    Create checkpoint objects using Web Services API
"""
from file.parser import *



def api_call( ip_addr, port, command, json_payload, sid ):
    url = 'https://' + ip_addr + ':' + str(port) + '/web_api/' + command
    request_headers = {
        "User-Agent": "python-api-wrapper",
        "Accept": "*/*",
        "Content-Type" : "application/json; charset=utf-8",
        "Content-Length": len(json_payload)
    }
    """if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    """
    resp = requests.post( url, json=json_payload, headers=request_headers, verify=False )
    return resp

def publish_result(sid=""):
    publish_result = api_call('192.168.56.2', 443, 'publish', {},sid)
    return publish_result

def add_network( name="", subnet="", mask="", sid=""):
    new_network_data = {"name":name, "subnet":subnet, "subnet-mask":mask}
    new_network_result = api_call( '192.168.56.2', 443,'add-network', new_network_data ,sid )
    return new_network_result

def login( usr, password ):
    payload = { 'user':usr, 'password' : password }
    response = api_call( '192.168.56.2', 443, 'login', payload, '' )
    return response

def logout( sid ):
    logout_result = api_call( '192.168.56.2', 443, 'logout', {},sid )
    return logout_result

class Checkpoint_writer():

    def __init__( self, parser=None, file_name="" ):
        self.parser = parser
        self.file_name = file_name

        #obj_list = self.parser.get_list_of_netAdresses()

        #[ print( obj.get_attrs() ) for obj in obj_list ]
        rt = login( 'admin', 'aze123..' )
        print( O+"login result: "+W )
        print( rt.content )

        rt = add_network( 'test_net', '192.168.1.0', '255.255.255.0', '' )
        print( rt )
        rt = api_call( '192.168.56.2', 443, 'show-hosts', {}, '' )
        print( rt.content )

        rt = publish_result()
        print( rt )
        rt = logout( '' )

        print( O+"logout result: "+W )
        print( rt )
