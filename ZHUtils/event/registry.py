# -*- coding: utf-8 -*-
# File    : registry.py
# Author  : Wang Zehao
# Email   : 
# Date    : Jul 24 2020
#
# Distributed under the MIT license

"""
This file is for register events
"""

import collections

__all__ = ['SimpleEventRegistry']

class SimpleEventRegistry(object):
    def __init__(self, allowed_events=None):
        """
        Args:
            allowed_events (set): set of event name (str)
        """
        self._allowed_events = allowed_events
        self._events = collections.defaultdict(list) # return [] when key not found
    
    def register(self, event, callback):
        if self._allowed_events is not None:
            assert event in self._allowed_events
        self._events[event].append(callback)

    def trigger(self, event, *args, **kwargs):
        if self._allowed_events is not None:
            assert event in self._allowed_events
        
        # get executable functions registered in current event
        for f in self._events[event]:
            f(*args, **kwargs)
