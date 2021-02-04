import socket
import json
import datetime
import traceback
import sys
import math

if len(sys.argv) < 4:
    sector_idx = 0
else:
    sector_idx = int(sys.argv[3])
if len(sys.argv) < 3:
    sector_type = 1
else:
    sector_type = int(sys.argv[2])
if len(sys.argv) < 2:
    rf_modules_idx = 0
else:
    rf_modules_idx = int(sys.argv[1])


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect the socket to the port where the server is listening
    #server_address = ('localhost',8000)
    server_address = ('192.168.137.11', 8000)
    print 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    buf_len = 10240
    
    # Send data
    data = {}
    # data['cmd'] = 'tx_sin'
    # data['args'] = {}
    
    data['cmd'] = 'set_pattern2'
    data['args'] =  {'sector_idx': sector_idx,
        'is_tx_sector': sector_type,
        'mag': "77777777777777777777777777777777",
        'phase': "00002010013011221002311223230001",
        'amp': "66666666",
        'sector_gain_idx': 5
    }
    message = json.dumps(data).encode('utf-8')
    print data
    
    a = datetime.datetime.now()
    while True:
    # for i in range(0, 64):
        sock.sendall(message)
        
        # Look for the response
        d = b''
        while True:
            d_tmp = sock.recv(buf_len)
            d += d_tmp
            if not d_tmp or d_tmp[-1] == '}' or d_tmp[-1] == ')' or d_tmp[-1] == ']':
                break
            
        if d:
            response = json.loads(d.decode('utf-8'))
            print(response)
#            ret = str(bin(response['rf_current_status'.encode()]))[-18:]
#            gain = ret[-12:-8]
#            sector = ret[-7:]
#            if ret[-18] == '1' and ret[-17] == '0':
#                print 'tx mode, gain index {}, sector {}'.format(int(gain, 2), int(sector, 2))
#            if ret[-18] == 'b' and ret[-17] == '1':
#                print 'rx mode, gain index {}, sector {}'.format(int(gain, 2), int(sector, 2))
            
        break
        # time.sleep(1)
        # time.sleep(20)
    
    b = datetime.datetime.now()
    delta = b - a
    print delta

except Exception as e:
    traceback.print_exc()
    print e
    print 'exiting'
finally:
    print 'connection close'
    sock.close()




