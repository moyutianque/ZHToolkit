# -*- coding: utf-8 -*-
# File    : io.py
# Author  : Wang Zehao
# Email   : 
# Date    : Jul 26 2020
#
# Distributed under the MIT license

"""
This file contains customized state_dict processing funcs
"""

import torch
import torch.nn as nn
from ZHUtils.logging import get_logger
from ZHUtils.utils.meta import as_cpu

logger = get_logger(__file__)

def state_dict(model, include=None, exclude=None, cpu=True):
    """
    Customized state_dict

    Args:
        model (nn.Module): cpu/gpu/parallel model
        include:
        exclude:
        cpu (bool): remove gpu wrappers
    """
    if isinstance(model, nn.DataParallel):
        model = model.module # remove parallel wrapper

    state_dict = model.state_dict()

    # TODO(Wang Zehao @ Jul 26 2020): complete include and exclude content 

    if cpu:
        state_dict = as_cpu(state_dict)

    # TODO(Wang Zehao @ Jul 26 2020): extra dict might need process

    return state_dict

def load_state_dict(model, state_dict, include=None, exclude=None):
    if isinstance(model, nn.DataParallel):
        model = model.module

    # TODO(Wang Zehao @ Jul 26 2020): complete include and exclude content

    # Build tensors
    for k,v in state_dict.items():
        if isinstance(v, np.ndarray):
            state_dict[k] = torch.from_numpy(v)
        
    err_msg = []
    own_state = model.state_dict() # states in a input model
    for name, param in state_dict.items():
        if name in own_state:
            if isinstance(param, nn.Parameter):
                # [jac comment]: backwards compatibility for serialized parameters
                # [zw]: a field is always kept for future version
                param = param.data
            try:
                own_state[name].copy_(param)
            except Exception:
                err_msg.append('While copying the parameter named {}, '
                               'whose dimensions in the model are {} and '
                               'whose dimensions in the checkpoint are {}.'
                               .format(name, own_state[name].size(),param.size()))

    # TODO(Wang Zehao @ Jul 26 2020): extra dict might need process

    missing = set(own_state.keys())-set(state_dict.keys())
    if len(missing) > 0:
        err_msg.append('Missing keys in state_dict: "{}".'.format(missing))
    
    unexpected = set(state_dict.keys())-set(own_state.keys())
    if len(unexpected) > 0:
        err_msg.append('Unexpected keys in state_dict: "{}".'.format(unexpected))

    if len(err_msg):
        raise KeyError('\n'.join(err_msg)) # newline split each error msg










