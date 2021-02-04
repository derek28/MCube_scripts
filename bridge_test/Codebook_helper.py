import scipy.io as sio

class Codebook_helper:
	def __init__(self, base_codebook_fname, base_codebook_len):
		self.base_codebook = {'mag':[],
							  'phase':[],
							  'amp':[]}

		self.full_mag_entry = '77777777777777777777777777777777'
		self.full_amp_entry = '66666666'
		self.null_mag_entry = '00000000000000000000000000000000'
		self.null_amp_entry = '00000000'

		# Load base codebook file
		base_phase_mat = sio.loadmat(base_codebook_fname)
		for b_idx in xrange(0, base_codebook_len):
			self.base_codebook['mag'].append(''.join(base_phase_mat['beam_weight'][0][b_idx][0][0].tolist()))
			self.base_codebook['phase'].append(''.join(base_phase_mat['beam_weight'][0][b_idx][0][1].tolist()))
			self.base_codebook['amp'].append(''.join(base_phase_mat['beam_weight'][0][b_idx][0][2].tolist()))

	# def correct_pha(self, pha, correction):
	# 	phal = list(pha)
	# 	for idx in xrange(0, 32):
	# 		phal[idx] = str((int(phal[idx]) + correction[idx]) % 4)
	# 	return ''.join(phal)

	def get_base_codebook(self):
		return self.base_codebook

	def get_null_codebook(self):
		null_codebook = {'mag':[],
						 'phase':[],
						 'amp':[]}
		for b_idx in xrange(0, 64):
			null_codebook['phase'].append(self.null_mag_entry)
			null_codebook['mag'].append(self.null_mag_entry)
			null_codebook['amp'].append(self.null_amp_entry)

		return null_codebook

	# def get_beam_combine(self, main_idx, side_idx):
	# 	main_entry = self.base_codebook['phase'][main_idx]
	# 	side_entry = self.base_codebook['phase'][side_idx]

	# 	main_codebook = {'mag':[],
	# 					 'phase':[],
	# 					 'amp':[]}

	# 	side_codebook = {'mag':[],
	# 					 'phase':[],
	# 					 'amp':[]}

	# 	main_codebook['phase'].append(self.null_mag_entry)
	# 	side_codebook['phase'].append(self.null_mag_entry)
	# 	main_codebook['mag'].append(self.null_mag_entry)
	# 	main_codebook['amp'].append(self.null_amp_entry)
	# 	side_codebook['mag'].append(self.null_mag_entry)
	# 	side_codebook['amp'].append(self.null_amp_entry)

	# 	for po in xrange(0, 4):
	# 		temp_side_entry = self.correct_pha(side_entry, [po]*32)
	# 		for count in xrange(0, 4):
	# 			main_codebook['phase'].append(main_entry)
	# 			side_codebook['phase'].append(temp_side_entry)
	# 			main_codebook['mag'].append(self.full_mag_entry)
	# 			main_codebook['amp'].append(self.full_amp_entry)
	# 			side_codebook['mag'].append(self.full_mag_entry)
	# 			side_codebook['amp'].append(self.full_amp_entry)

	# 	return main_codebook, side_codebook

