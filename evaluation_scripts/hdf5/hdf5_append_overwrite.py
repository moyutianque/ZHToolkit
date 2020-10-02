
# %% Verify resize and append/overwrite on existing array
import numpy as np
import h5py

x, y = 100,4

# create
np.random.seed(0)
a = np.random.random(size=(x, y))
h5f = h5py.File('features.h5', 'w')
h5f.create_dataset('bboxes', data=a, dtype='f', chunks=True, maxshape=(None, 4))
print(a[79][0:4])
print(a[80][0:4])
print(a[81][0:4])
# ==> [0.42053947 0.55736879 0.86055117 0.72704426]
# ==> [0.27032791 0.1314828  0.05537432 0.30159863]
# ==> [0.26211815 0.45614057 0.68328134 0.69562545]
# shape (100, 4)
h5f.close()

# %% append
bboxes = np.ones((10,4))
accum_idx = 80
with h5py.File('features.h5', 'a') as f:
	dset_bboxes = f['bboxes']
	dset_bboxes.resize((accum_idx+bboxes.shape[0]), axis=0)
	dset_bboxes[-bboxes.shape[0]:]=bboxes
	print(dset_bboxes[79][0:4])
	print(dset_bboxes[80][0:4])
	print(dset_bboxes[81][0:4])
	""" ==>
	[0.42053947 0.5573688  0.8605512  0.7270443 ]
	[1. 1. 1. 1.]
	[1. 1. 1. 1.]
	"""
	print(dset_bboxes.shape)
	# ==> (90,,4)

# %% read again
with h5py.File('features.h5', 'r') as f:
	dset_bboxes = f['bboxes']
	print(dset_bboxes[79][0:4])
	print(dset_bboxes[80][0:4])
	print(dset_bboxes[81][0:4])
	""" ==>
	[0.42053947 0.5573688  0.8605512  0.7270443 ]
	[1. 1. 1. 1.]
	[1. 1. 1. 1.]
	"""
	print(dset_bboxes.shape)
	# ==> (90,,4)