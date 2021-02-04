import Codebook_helper
import Sparrow
import traceback
import ast
import scipy.io as sio
import os
import sys
import threading
import socket
import time
import struct
from array import array

class RSSSocket:

	def __init__(self):
		# self.ap_addr = [('192.168.137.12', 10001), ('192.168.137.13', 10001)]
		self.ap_addr = [('192.168.137.12', 10001)]
		self.ap_num = len(self.ap_addr)
		self.rx_addr = ('192.168.137.3', 10000)

		self.ap = []
		for ii in range(self.ap_num):
			self.ap.append(Sparrow.Sparrow(self.ap_addr[ii]))
		self.rx = Sparrow.Sparrow(self.rx_addr)

		self.cb_dir = ['csi_cb1.mat', 'csi_cb2.mat', 'scan2d_cb1.mat', 'scan2d_cb2.mat', \
			'csi08_cb1.mat', 'csi08_cb2.mat', 'csi12_cb1.mat', 'csi12_cb2.mat', \
			'csi24_cb1.mat', 'csi24_cb2.mat', 'csi32_cb1.mat', 'csi32_cb2.mat', \
			'csi45_cb1.mat', 'csi45_cb2.mat', 'csi60_cb1.mat', 'csi60_cb2.mat', \
			'csi75_cb1.mat', 'csi75_cb2.mat', 'csi105_cb1.mat', 'csi105_cb2.mat', \
			'csi120_cb1.mat', 'csi120_cb2.mat', 'csi135_cb1.mat', 'csi135_cb2.mat']
		self.cb_num = len(self.cb_dir)
		self.beam_num = 64
		self.cb_helper = []
		self.cb = []
		for ii in range(self.cb_num):
			self.cb_helper.append(Codebook_helper.Codebook_helper(self.cb_dir[ii], self.beam_num))
			self.cb.append(self.cb_helper[ii].get_base_codebook())
		self.cb0 = self.cb_helper[0].get_null_codebook()

		self.p = [1]

		for ii in range(self.ap_num):
			self.ap[ii].connect()
		self.rx.connect()

		for ii in range(self.ap_num):
			self.ap[ii].load_codebook(self.cb0, 0)
			for jj in range(self.cb_num):
				self.ap[ii].load_codebook(self.cb[jj], jj+1)
			self.ap[ii].set_codebook_active(0, range(0,8))

	def to_file(self, path):
		# snr = []
		ts = []
		# fname = path + '.mat'
		fout = open(path, 'wb')
		try:
			while True:
				temp = []
				for ii in range(self.ap_num):
					for jj in range(self.cb_num):
						self.ap[ii].set_codebook_active(jj+1,self.p)
						time.sleep(1e-3)
						temp.append(self.rx.per_beam_snr())
					self.ap[ii].set_codebook_active(0,self.p)
					time.sleep(1e-3)

				print '%d RSS received.' % (len(ts)+1)
				# print temp
				t = time.time()
				fout.write(struct.pack('d', t))
				for ii in xrange(len(temp)):
					array('L', temp[ii]).tofile(fout)
				# snr.append(temp)
				ts.append(t)
				
		except Exception as e:
			traceback.print_exc()
			print e
		# finally:
		# 	sio.savemat(fname, {'snr': snr, 'ts': ts})
		# 	for ii in range(self.ap_num):
		# 		self.ap[ii].close()
		# 	self.rx.close()


class RSSThread(threading.Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
		super(RSSThread,self).__init__()
		self.target = target
		self.name = name
		self.fp = args[0]

	def run(self):
		rss_soc = RSSSocket()
		rss_soc.to_file(direct + '/' + self.fp + '/rss.dat')


class PointCloudSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buf_len = 10240
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def listen(self):
        # try:
        #     sp.check_call('adb reverse tcp:8000 tcp:8000')
        # except Exception as e:
        #     print e
        # time.sleep(1)
        self.sock.bind(("0.0.0.0", 9000))
        # self.sock.bind(("127.0.0.1", 8000))
        self.sock.listen(1)
        print "PointCloudSocket: Start listen."
        (self.con_sock, self.address) = self.sock.accept()
        print "PointCloudSocket: Connection success."

    def to_file(self, path):
        fout = open(path, 'wb')
        byte_read = 0;
        while True:
            d_tmp = self.con_sock.recv(self.buf_len)
            fout.write(d_tmp)
            if ((byte_read + len(d_tmp)) >> 20) > (byte_read >> 20):
                print "PointCloudSocket: Read %f MB data." % ((byte_read + len(d_tmp)) >> 20)
            byte_read += len(d_tmp)

class PointCloudThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(PointCloudThread,self).__init__()
        self.target = target
        self.name = name
        self.fp = args[0]

    def run(self):
        pc_soc = PointCloudSocket()
        pc_soc.listen()
        pc_soc.to_file(direct + '/' + self.fp + '/pc.dat')

direct = '2d_loc'

if __name__ == '__main__':
	prefix = sys.argv[1]
	if not os.path.isdir(direct + '/' + prefix):
		os.mkdir(direct + '/' + prefix)

	# pthread = PointCloudThread(name='PC Data', args=[prefix])
	# pthread.daemon = True
	# pthread.start()

	# input()

	rthread = RSSThread(name='RSS Data', args=[prefix])
	rthread.daemon = True
	rthread.start()

	input()
