# -*- coding: utf-8 -*-
# File    :
# Author  : Wang Zehao
# Email   : 
# Date    : Jul 24 2020
#
# Distributed under the MIT license

"""
This file is customized trainer wrapper also named as
the TrainEnv
"""

import torch
import torch.nn as nn

import time
import os
from ZHUtils.logging import get_logger
from ZHUtils.event.registry import SimpleEventRegistry

from ZHTorch.io import state_dict,load_state_dict
from ZHTorch.utils.meta import as_cpu, as_tensor, as_float

logger = get_logger(__file__)

__all__ = ['TrainEnv']


def cuda_time(sync=True):
    """ sync parallel process and return time"""
    if sync:
        torch.cuda.synchronize()
    return time.time()

def default_reduce_func(k,v):
    """ [guess] for syncronize different thread's results """
    if torch.is_tensor(v):
        return v.mean()
    return v

Class TrainEnv(object):
    def __init__(self, model, optimizer):
        self._model = model
        self._optimizer = optimizer

        self._train_loader = None
        self._val_loader = None
        
        # [Observer/Event] collect data or treat as a hook to modify
        allowed_events = {
            'epoch:before', 'epoch:after',
            'step:before', 'step:after',
            'forward:before', 'forward:after',
            'backward:before', 'backward:after',
        }
        self._event_manager = SimpleEventRegistry(allowed_events) 

    @property
    def model(self):
        return self._model
    
    @property
    def model_unwrapped(self):
        """ get the model without data parallel wrap """
        model = self._model
        if isinstance(model, nn.DataParallel):
            model = model.module
        return model

    @property
    def optimizer(self):
        return optimizer

    def register_event(self, name, callback):
        """
        Args:
            name (str): event name
            callback (func): event related func or module
        """
        logger.info('Register trainer event: name={}, callback={}.'
                    .format(name, callback.__module__ + '.' + callback.__name__))
        return self._event_manager.register(name, callback) 
       
    def trigger_event(self, name, *args, **kwargs):
        """
        trigger registered event by name
        
        Args:
            name (str): event name
            args and kwargs: event inputs
        """
        self._event_manager.trigger(name, *args, **kwargs)

    def save_checkpoint(self, filename, extra=None): 
        model = self._model
        
        # customized state_dict save model without datapallel wrapper
        stat = {
            'model': state_dict(model, cpu=True),
            'optimizer': as_cpu(self._optimizer.state_dict()),
            'extra': extra
        }
        try:
            torch.save(state, filename)
            logger.info('Checkpoint saved: "{}".'.format(filename))
        except Exception:
            logger.exception('Error occurred when dump checkpoint "{}".'
                                .format(filename))

    def load_checkpoint(self, filename):
        if os.path.isfile(filename):
            model = self._model
            if isinstance(model, nn.DataParallel):
                model = model.module

            try:
                checkpoint = torch.load(filename)
                # use customized state_dict loader for model parameters
                load_state_dict(model, checkpoint['model'])

                self._optimizer.load_state_dict(checkpoint['optimizer'])
                logger.critical('Checkpoint loaded: {}.'.format(filename))
                return checkpoint['extra']
            except Exception:
                logger.exception('Error occurred when load checkpoint "{}".'.format(filename))
        else:
            logger.warning('No checkpoint found at: "{}".'.format(filename))
        return None

    def step(self, feed_dict, grad_clip=0., reduce_func=default_reduce_func, 
                cast_tensor=False, measure_time=False):
        """
        [Template Method]
        Training: Forward and optimize one step

        Args:
            feed_dict (dict):
            grad_clip (float):
            reduce_func:
            cast_tensor (bool): whether to transfer data in feed_dict to tensors
            measure_time (bool): whether to record time
        """
        # if step method implemented under model
        if hasattr(self.model, 'train_step'):
            return self.model.train_step(self.optimizer, feed_dict) 

        assert self._model.training, '[Error] model is not set to train-mode'
        extra=dict()

        self.trigger_event('step:before', self)

        if cast_tensor:
            feed_dict = as_tensor(feed_dict)      

        if measure_time:
            end_time = cuda_time(sync=True)
        
        """ 1. forward data """
        # if event not registered, nothing will happen in trigger_event
        self.trigger_event('forward:before', self, feed_dict)
        loss, monitors, output_dict = self._model(feed_dict)
        self.trigger_event('forward:after', self, feed_dict, loss, monitors, output_dict)
        
        if measure_time:
            extra['time/forward'] = cuda_time(sync=True) - end_time
            end_time = cuda_time(sync=False)

        """ 2. loss reduction """
        loss = reduce_func('loss', loss) 
        # TODO(Wang Zehao @ Jul 27 2020): know more about monitors
        monitors = {k: reduce_func(k,v) for k,v in monitors.items()}

        loss_f = as_float(loss)
        monitors_f = as_float(monitors)

        if measure_time:
            # record the time for reduce operation on Loss
            extra['time/loss'] = cuda_time(sync=True) - end_time
            end_time = cuda_time(sync=False)
        
        """ 3. backward data """
        self._optimizer.zero_grad()
        self.trigger_event('backward:before', self, feed_dict, loss, monitors, output_dict)
        if loss.requires_grad:
            loss.backward()
            if grad_clip > 0:
                from torch.nn.utils.clip_grad import clip_grad_norm_
                clip_grad_norm_(self.model.parameters(), grad_clip)

        if measure_time:
            extra['time/backward'] = cuda_time(sync=True) - end_time
            end_time = cuda_time(sync=False)

        """ 4. optimizer step """
        self.trigger_event('backward:after', self, feed_dict, loss, monitors, output_dict)
        if loss.requires_grad:
            self._optimizer.step()

        if measure_time:
            extra['time/optimize'] = cuda_time(sync=True) - end_time
            end_time = cuda_time(sync=False)

        self.trigger_event('step:after', self)
        
        return loss_f, monitors_f, output_dict, extra


    def evaluate(self, feed_dict, cast_tensor=False):
        """
        [Template Method]
        Evaluation
        """
        assert not self._model.training, "[Error] model is not set to eval-mode"
        begin = time.time()
        if cast_tensor:
            feed_dict = as_tensor(feed_dict)
        with torch.no_grad():
            output_dict = self._model(feed_dict) 
        end = time.time()
        return output_dict, dict(gpu_time=end-begin)
















