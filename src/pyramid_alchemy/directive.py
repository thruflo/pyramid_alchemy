# -*- coding: utf-8 -*-

"""Provide the ``add_model_method`` directive."""

__all__ = [
    'add_model_method',
]

class AddModelMethod(object):
    def __init__(self, **kwargs):
        pass
    
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
    

add_model_method = AddModelMethod()
