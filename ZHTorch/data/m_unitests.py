# -*- coding: utf-8 -*-
# File    : unitests.py
# Author  : Wang Zehao
# Email   : 
# Date    : Aug 03 2020
#
# Distributed under the MIT license

"""

"""
import unittest


class TestDataset(unittest.TestCase):
    def test_BaseVLDataset(self):
        from dataset import BaseVLDataset
        img_path = '/esat/jade/tmp/zwang/dataset/GQA/images'
        text_path = '/esat/jade/tmp/zwang/dataset/GQA/questions1.3' 
        dataset = BaseVLDataset(img_path, text_path)
        dataset.info()

if __name__=='__main__':
    unittest.main()
