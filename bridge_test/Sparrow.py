import socket
import json
import time
import datetime
import ast

class Sparrow:
	def __init__(self, address, buf_len=10240):
		self.address = address
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.buf_len = buf_len

	def connect(self):
		self.sock.connect(self.address)

	def close(self):
		self.sock.close()

	def send_cmd(self, cmd, args):
		data = {}
		data['cmd'] = cmd
		data['args'] = args
		m = json.dumps(data).encode('utf-8')
		st = time.time()	# Timer start
		self.sock.sendall(m)
		# print 'Send command %s' % cmd

		d = b''
		while True:
			d_tmp = self.sock.recv(self.buf_len)
			d = d + d_tmp
			if not d_tmp or d_tmp[-1] == '}' or d_tmp[-1] == ']' or d_tmp[-1] == ')':
				break
		et = time.time()	# Timer end
		# print 'Time Elapsed: %.4f' % (et-st)
		
		return ast.literal_eval(d)

	def load_codebook(self, codebook, codebook_idx):
		cmd = 'set_codebook_block'
		args = {'codebook_idx': codebook_idx,
				'mag':codebook['mag'],
				'phase':codebook['phase'],
				'amp':codebook['amp']}

		return self.send_cmd(cmd, args)

	def set_codebook_active(self, codebook_idx, panel_idx):
		p = 0
		for ii in xrange(0, len(panel_idx)):
			p = p + 2**panel_idx[ii]

		cmd = 'set_codebook_active'
		args = {'codebook_idx':codebook_idx,
				'rf_modules_vec':p,
				'store_data':1}

		return self.send_cmd(cmd, args)

	def per_beam_snr(self):
		cmd = 'per_beam_snr'
		args = {}

		return self.send_cmd(cmd, args)

	def per_beam_rss(self):
		cmd = 'per_beam_snr'
		args = {}

		return self.send_cmd(cmd, args)

