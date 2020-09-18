# -*- coding: utf-8 -*-
# File    : meta.py
# Author  : Wang Zehao
# Email   : 
# Date    : Jul 26 2020
#
# Distributed under the MIT license

"""

"""
import six
import collections

def stmap(func, iterable):
    """ apply func on iterable object"""
    if isinstance(iterable, six.string_types):
        return func(iterable)
    elif isinstance(iterable, (collections.Sequence, collections.UserList)):
        return [stmap(func,v) for v in iterable]
    elif isinstance(iterable, collections.Set):
        return {stmap(func,v) for v in iterable]
    elif isinstance(iterable, (collections.Mapping, collections.UserDict)):
        return {k: stmap(func,v) for k,v in iterable.items()}
    else:
        return func(iterable)

