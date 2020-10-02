#%%
import timeit
import psutil
class execution_timer:
    def __enter__(self):
        self.ts = timeit.default_timer()
        self.ram_s = psutil.virtual_memory()  # physical memory usage

    def __exit__(self, type, value, traceback):
        te = timeit.default_timer()
        ram_e = psutil.virtual_memory()  # physical memory usage
        print(f'[INFO] Execution time for 10000 query: {te-self.ts} seconds')
        print(f'[INFO] RAM changes: {(ram_e.used-self.ram_s.used)/(1024*1024)} MB')

# %% Verify how to load a batch of data (each need several rows)
import numpy as np
import h5py

x, y = 100,4

# create
np.random.seed(0)
a = np.random.random(size=(x, y))
h5f = h5py.File('features.h5', 'w')
h5f.create_dataset('bboxes', data=a, dtype='f', chunks=True, maxshape=(None, 4))
print(a[1:5])
print()
print(a[50:55])
print()
print(a[70:77])
print()
# ==> [0.42053947 0.55736879 0.86055117 0.72704426]
# ==> [0.27032791 0.1314828  0.05537432 0.30159863]
# ==> [0.26211815 0.45614057 0.68328134 0.69562545]
# shape (100, 4)
h5f.close()

# %% read and indexing
with h5py.File('features.h5', 'r') as f:
	dset_bboxes = f['bboxes']
	slices = [(1,5), (50,55), (70,77)]
	for s in slices:
		dset_bboxes[s[0]:s[1]]


# %% evaluation on heavily loading data

import numpy as np
import h5py

x, y = 100000,4

# create
np.random.seed(0)
a = np.random.random(size=(x, y))
h5f = h5py.File('features.h5', 'w')
h5f.create_dataset('bboxes', data=a, dtype='f', chunks=True, maxshape=(None, 4))
print(a[1:5])
print()
print(a[50:55])
print()
print(a[70:77])
print()
# ==> [0.42053947 0.55736879 0.86055117 0.72704426]
# ==> [0.27032791 0.1314828  0.05537432 0.30159863]
# ==> [0.26211815 0.45614057 0.68328134 0.69562545]
# shape (100, 4)
h5f.close()

# %% read and indexing
slices = []
for i in range(10000):
	a = np.random.randint(0,100000//3)
	b = np.random.randint(a, 100000)
	slices.append( (a,b) )

# %% # 16s for 10000 query
with execution_timer():
	with h5py.File('features.h5', 'r') as f:
		dset_bboxes = f['bboxes']
		for s in slices:
			dset_bboxes[s[0]:s[1]]

