# -*- coding: utf-8 -*-
# File    : file_info.py
# Author  : Wang Zehao
# Email   : 
# Date    : Aug 05 2020
#
# Distributed under the MIT license

"""

"""
import json

PREFIXES = ['', '   ', '      ', '         ', '            ']
def print_json_struct(v, depth=0, max_depth=5, prefix_list:list=PREFIXES):
    if depth>=max_depth:
        return
    
    if isinstance(v, dict):
        print('{}Dict with {} keys: \n{}{}\n{}^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'.format(
            prefix_list[depth], len(v.keys()), prefix_list[depth], 
            list(v.keys()), prefix_list[depth]) 
        )
        for k in v.keys():
            print('{}-- {}:'.format(
                prefix_list[depth], k )
            )
            print_json_struct(v[k], depth+1, max_depth, prefix_list)
            print('{}=========================================================='.format(
                prefix_list[depth])
            )
            
    elif isinstance(v, (tuple, list)):
        if len(v)!=0:
            print('{}List with {} elements of type {}:\n{}e.g.'.format(
                prefix_list[depth], len(v), type(v[0]).__name__,prefix_list[depth])
            )
            
            print_json_struct(v[0], depth, max_depth, prefix_list)
        else:
            print('{}[Empty warning]List with {} elements: \n    '.format(
                prefix_list[depth], len(v))
            )
    else:
        print('{}Value({}): e.g. {}'.format(prefix_list[depth], type(v).__name__, v))
