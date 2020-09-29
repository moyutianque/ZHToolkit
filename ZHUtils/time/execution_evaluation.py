#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File    : execution_evaluation.py
# Author  : Wang Zehao
# Email   :
# Date    : Sep 29 2020
#
# Distributed under the MIT license

"""
Here are tools in decorator form or wrapper form, for evaluating execution time and memory usage
"""
# ADD (Zehao Wang @ Sep 29 2020): timer temporary write here
import timeit
import psutil


def execution_time(method):
    """ decorator style """

    def time_measure(*args, **kwargs):
        ts = timeit.default_timer()
        result = method(*args, **kwargs)
        te = timeit.default_timer()

        print(f'Excution time of method {method.__name__} is {te - ts} seconds.')
        return result

    return time_measure


class execution_timer:
    def __enter__(self):
        self.ts = timeit.default_timer()
        self.ram_s = psutil.virtual_memory()

    def __exit__(self, exc_type, exc_val, exc_tb):
        te = timeit.default_timer()
        ram_e = psutil.virtual_memory()
        print(f'[INFO] Execution time: {te - self.ts} seconds...')
        print(
            f'[INFO] RAM change: {(ram_e.used - self.ram_s.used) / (1024 * 1024)} MB => +{ram_e.percent - self.ram_s.percent}% ...')

# ENDMODIFY
