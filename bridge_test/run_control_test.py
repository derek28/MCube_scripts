#!/usr/bin/env python3

import socket
import sys
import json
import datetime

def do_cmd(cmd, args):
    data = {}
    data['cmd'] = cmd
    data['args'] = args
    message = (json.dumps(data)).encode('utf-8')
    a = datetime.datetime.now()
    while True:
    # for i in range(0, 64):
        sock.sendall(message)
        
        # Look for the response
        d = b''
        while True:
            d_tmp = sock.recv(buf_len)
            d += d_tmp
            d_tmp = d_tmp.decode("utf-8") #Py3 compatibility
            if not d_tmp or d_tmp[-1] == '}' or d_tmp[-1] == ')' or d_tmp[-1] == ']':
                break
            
        if d:
            response = json.loads(d.decode('utf-8'))
            return response
            
        break
        # time.sleep(1)
        # time.sleep(20)
    
    b = datetime.datetime.now()
    delta = b - a
    #print delta

# Create a TCP/IP socket
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for i in range(1):
    # Connect the socket to the port where the server is listening
    server_address = ('192.168.137.13', 8000)
    sock.connect(server_address)
    print('connected to %s port %s' % server_address)
    buf_len = 10240

    bb_gain = 9
    rf_gain = 5
    n_err = 0
    for sector_id in range(0,100):
        do_cmd('rx_mode', {'rf_gain_index':bb_gain, 'rx_bb_gain_row_num':rf_gain, 'rf_sector_id':sector_id})
        status_resp = do_cmd('get_rf_status', {'rfc_id': 0xff})
        ret = str(bin(status_resp['rf_current_status']))[-18:]
        gain = int(ret[-12:-8], base=2)
        sector = int(ret[-7:], base=2)
        err = (sector != sector_id) or (gain != rf_gain)
        print("gain", gain, "sector", sector, "err", err)
        if err: n_err += 1
    print(do_cmd('rx_mode', {'enable':0, 'rf_gain_index':bb_gain, 'rx_bb_gain_row_num':rf_gain, 'rf_sector_id':0}))
    print("total errors", n_err)
