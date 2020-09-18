# -*- coding: utf-8 -*-
# File    : meta.py
# Author  : Wang Zehao
# Email   : 
# Date    : Jul 26 2020
#
# Distributed under the MIT license

"""

"""

import torch
import six
import numpy as np

from ZHUtils.utils.meta import stmap

# [guess] exemption type
SKIP_TYPES = six.string_types


def _as_tensor(obj):
    if isinstance(obj, SKIP_TYPES):
        return obj
    elif torch.is_tensor(obj):
        return obj
    return torch.from_numpy(np.array(obj))

def as_tensor(obj):
    return stmap(_as_tensor, obj)


def _as_cpu(obj):
    if torch.is_tensor(obj):
        return obj.cpu()
    return obj.cpu()

def as_cpu(obj):
    return stmap(_as_cpu, obj)

def _as_numpy(obj):
    if isinstance(obj, SKIP_TYPES):
        return obj

    if torch.is_tensor(obj):
        return obj.cpu().numpy()

    return np.array(obj)

def as_numpy(obj):
    return stmap(_as_numpy, obj)

def _as_float(obj):
    if isinstance(obj, SKIP_TYPES):
        return obj
    if torch.is_tensor(obj):
        return obj.item()
    arr = as_numpy(obj)
    assert arr.size == 1
    return float(arr)

def as_float(obj):
    return stmap(_as_float, obj)

