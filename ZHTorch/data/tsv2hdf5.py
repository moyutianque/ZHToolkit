import numpy as np
import csv

def tsv2hdf5(tsv_name, hdf5_name, topk=None):
    """
    Convert provided large tsv file of Bottom-up paper to hdf5 file. 
    Use img_id as key every information are stored in byte string. 
    Convert to normal string by calling .decode("ascii")
    """
    import h5py

    with h5py.File(hdf5_name, "w") as h5file:
        with open(tsv_name) as f:
            reader = csv.reader(f, delimiter='\t')
            for i, datum in enumerate(reader):
                img_id = datum[0]
                
                dt = h5py.string_dtype(encoding='ascii') 
                datum = np.array(datum[1:],dtype=dt)
                h5file.create_dataset(img_id,(9,), data=datum)
                if topk is not None and i == topk:
                    break
                    

def cmp_tsvAndhdf5(tsv_name, hdf5_name, topk=None):
    """
    Test consistency of original tsv and hdf5
    """
    import h5py
    with h5py.File(hdf5_name, "r") as h5file:
        with open(tsv_name) as f:
            reader = csv.reader(f, delimiter='\t')
            for i, datum in enumerate(reader):
                img_id = datum[0]
                h5datum = h5file[img_id]
                
                for j, item in enumerate(datum[1:]):
                    assert str(item) == h5datum[j].decode("ascii") , f"{item} != {h5datum[j]}"
                    
                if topk is not None and i == topk:
                    break
                    
def _report_time_efficiency(hdf5_name='/esat/jade/tmp/zwang/dataset/GQA/GQA_h5/vg_gqa_obj36.h5'):
    """
    Report total time cost and average time per batch (size 100, not parallel)
    
    Results: [INFO] Total time cost 60.55142737249844, average time per batch (size 100, not parallel) = 0.06055142737249844
    """
    # We test on trainval set of GQA
    import h5py
    with h5py.File(hdf5_name,'r') as hf:
        img_ids = list(hf.keys())
    print(f'[INFO] There are {len(img_ids)} images in trainval set')
    
    assert len(img_ids) < 1000*100, "Please use dataset larger than 1000*100 datum, otherwise change shuffle with sample"
    
    import timeit
    np.random.seed(666)
    np.random.shuffle(np.array(img_ids))
    
    tot_time = 0.
    for i in range(0, 1000 * 100, 100):
        tic = timeit.default_timer()
        dataList = list()
        for j in range(100):
            with h5py.File(hdf5_name, "r") as hf:
                h5data = hf[img_ids[i+j]]
                dataList.append(h5data)
        toc = timeit.default_timer()
        tot_time += (toc-tic)

    print(f'[INFO] Total time cost {tot_time}, average time per batch (size 100, not parallel) = {tot_time/1000.}')
    