# -*- coding: utf-8 -*-
# File    : registry.py
# Author  : Wang Zehao
# Email   : 
# Date    : Jul 27 2020
#
# Distributed under the MIT license

"""
This file contains all the default class for registry tasks
which can handle a list of callback (a special term in parallel computing)
and fallback (when one callback undefined)
"""

import collections
import threading

class Registry(object):
    """ The base class for different type of registry """
    # change jac's double _ to single _, 
    # because do not find benifit for customized special variable
    _FALLBACK_KEY = '__fallback__' 

    # _registry=None # seems not used at all

    def __init__(self):
        self._init_registry()

    def _init_registry(self):
        self._registry=dict()

    @property
    def fallback(self):
        return self._registry.get(self._FALLBACK_KEY, None)

    def set_fallback(self, value):
        """ fallback is used when exception raised, e.g. undefined callback 
            the value can be a function call
        """
        self._registry[self._FALLBACK_KEY]=value
        return self

    def register(self, entry, value):
        self._registry[entry] = value
        return self

    def unregister(self, entry):
        return self._registry.pop(entry, None)

    def has(self, entry):
        return entry in self._registry

    def lookup(self, entry, fallback=True, default=None):
        """ if entry not in registry return fall-back value
             else return entry value 
        """
        fallback_value=default
        if fallback:
            fallback_value = self._registry.get(self._FALLBACK_KEY, default)
        return self._registry.get(entry, fallback_value)
    
    def keys(self):
        return list(self._registry.keys())

    def items(self):
        return list(self._registry.items()) 

class RegistryGroup(object):
    """ The base class for different registry group 
        Registry group is used to manage tasks in two level hierarchy    
    """
    _v_base_class = Registry

    def __init__(self):
        self._init_registry_group()

    def _init_registry_group(self):
        v_base_class = type(self)._v_base_class
        self._registries = collections.defaultdict(v_base_class)

    def __gititem__(self, item):
        return self._registries[item]
    
    def keys(self):
        return list(self._registries.keys())
    
    def register(self, registry_name, entry, value, **kwargs):
        # TODO(Wang Zehao @ Jul 27 2020): if kwargs used, add a comment here
        return self._registries[registry_name].register(entry, value, **kwargs)

    def lookup(self, registry_name, entry, fallback=True, default=None):
        return self._registries[registry_name].lookup(entry, fallback, default)

class DefaultRegistry(Registry):
    _v_base_class = dict # value class for a new entry

    # override
    def _init_registry(self): 
        v_base_class = type(self)._v_base_class
        self._registry = collections.defaultdict(v_base_class)
    
    # override
    def lookup(self, entry, fallback=False, default=None):
        assert fallback is False and default is None,\
                "[Error] DefaultRegistry class not allow fallback"
        return self._registry[entry]

    def __getitem__(self, item):
        return self.lookup(item)


class CallbackRegistry(Registry):
    """ [zw] Allow to define a highest priority entry, named super callback

    A callable manager utils.
    
    If there exists a super callback, it will block all callbacks.
    A super callback will receive the called name as its first argument.

    Then the dispatcher will try to call the callback by name.
    If such name does not exists, a fallback callback will be called.

    The fallback callback will also receive the called name as its first argument.

    Examples:
    >>> registry = CallbackRegistry()
    >>> callback_func = print
    >>> registry.register('name', callback_func)  # register a callback.
    >>> registry.dispatch('name', 'arg1', 'arg2', kwarg1='kwarg1')  # dispatch.
    """
    
    def __init__(self):
        super().__init__()
        self._super_callback = None
    
    @property
    def super_callback(self):
        return self._super_callback

    def set_super_callback(self, callback):
        self._super_callback = callback
        return self

    @property
    def fallback_callback(self):
        return self.fallback

    def set_fallback_callback(self, callback):
        return self.set_fallback(callback)

    def dispatch(self, name, *args, **kwargs):
        if self._super_callback is not None:
            return self._super_callback(self, name, *args, **kwargs)
        return self.dispatch_direct(name, *args)
    
    def dispatch_direct(self, name, *args, **kwargs):
        """Dispatch by name, ignoring the super callback."""
        callback = self.lookup(name, fallback=False)
        if callback is None:
            if self.fallback_callback is None:
                raise ValueError('Unknown callback entry: "{}".'.format(name))
            return self.fallback_callback(self, name, *args, **kwargs)
        return callback(*args, **kwargs)


# TODO(Wang Zehao @ Jul 27 2020): add LockRegistry    






















