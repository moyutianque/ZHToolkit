# -*- coding: utf-8 -*-
# File    : dataset.py
# Author  : Wang Zehao
# Email   : 
# Date    : Aug 03 2020
#
# Distributed under the MIT license

"""
Abstract class for different type of dataset
"""
import os


class Dataset(object):
    """An abstract class representing a Dataset.

    All other datasets should subclass it. All subclasses should override
    ``__len__``, that provides the size of the dataset, and ``__getitem__``,
    supporting integer indexing in range from 0 to len(self) exclusive.
    """

    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __add__(self, other):
        from torch.utils.data.dataset import ConcatDataset
        return ConcatDataset([self, other])



class FilterableVLDataset(Dataset):
    """ Base class for Visual-Language task datasets """
    def __init__(self, img_path, text_path):
        """
        Args:
            img_path(str): image folder with (jpg or png files) or (h5 or csv features)
            text_path(str): language input folder with json files
        """
        super().__init__()
        self.img_path = img_path
        self.text_path = text_path
    
        self.metainfo_catch=dict()
        self.metakeys = set()
    
    def add_metakey(self, key):
        self.metakeys.add(key)

    def get_metainfo(self, index):
        """
        Args:
            index (int): item index
        """
        if index not in self.metainfo_catch:
            self.metainfo_catch[index] = self._filter_metainfo(index)
        return self.metainfo_catch[index]

    def _filter_metainfo(self, index):
        """ Need to be overriden: filter out not needed info """
        raise NotImplementedError

    def info(self): 
        extension_set = set()
        img_list = list()
        for f in os.listdir(self.img_path):
            if os.path.isfile(os.path.join(self.img_path, f)):
                if f.lower().endswith( ('.png', '.jpg', '.jpeg')):
                    img_list.append(f)
                    extension_set.add(f.split('.')[-1]) 
        
        print(f'In dataset {self.__class__.__name__}:\n'
              f'-- {len(img_list)} images with type {extension_set}')

        extension_set = set()
        text_list = list()
         
        for f in os.listdir(self.text_path):
            if os.path.isfile(os.path.join(self.text_path, f)):
                if f.lower().endswith( '.json' ):
                    text_list.append(f)
                    extension_set.add(f.split('.')[-1]) 
        print(f'-- {len(text_list)} text files with type {extension_set}')
        





        


