"""
In this file we aim to evaluate boolean array size and other
dtype. How much memory does they actually take
"""
# %%
import numpy as np

# %% boolean array
bool_arr = np.ones((10,10,3), dtype=bool)
print(f'{bool_arr.nbytes} bytes for boolean array shape [10,10,3]')

trim_off = - (len(bool_arr.flat) % 8) # trimed length is necessary for unpack
bool_arr_packed = np.packbits(bool_arr.flat, axis=0)
print(f'{bool_arr_packed.nbytes} bytes for packed boolean array')
bool_arr_unpacked = np.unpackbits(bool_arr_packed, count=trim_off,axis=0).reshape((10,10,3))
print(f'{bool_arr_unpacked.nbytes} bytes for unpacked boolean array')

# %% 
