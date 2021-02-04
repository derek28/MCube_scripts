#! /usr/bin/env python3

import socket
import sys
import json
import datetime
import traceback

if len(sys.argv) < 2:
    rfc_enable_vector = 0x0C
else:
    rfc_enable_vector = int(sys.argv[1])


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect the socket to the port where the server is listening
    server_address = ('192.168.137.13', 8000)
    #server_address = ('localhost', 8000)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    buf_len = 10240
    
    # Send data
    data = {}
    # data['cmd'] = 'tx_sin'
    # data['args'] = {}
    
    data['cmd'] = 'set_rf_module'
    data['args'] = {'rfc_enable_vec':rfc_enable_vector}

    #data['args'] = {}
       
    message = json.dumps(data).encode('utf-8')
    print (data)
    
    a = datetime.datetime.now()
    while True:
    # for i in range(0, 64):
        sock.sendall(message)
        
        # Look for the response
        d = b''
        while True:
           # sock.settimeout(1.0)
            d_tmp = sock.recv(buf_len)
            d += d_tmp
            if not d_tmp or d_tmp[-1] == ord('}') or d_tmp[-1] == ord(')') or d_tmp[-1] == ord(']'):
                break
            
        if d:
            response = json.loads(d.decode('utf-8'))
            print (response)
            
        break
        # time.sleep(1)
        # time.sleep(20)
    
    b = datetime.datetime.now()
    delta = b - a
    print (delta)

except Exception as e:
    traceback.print_exc()
    print (e)
    print ('exiting')
finally:
    print ('connection close')
    sock.close()




