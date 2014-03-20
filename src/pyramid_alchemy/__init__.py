# -*- coding: utf-8 -*-

"""Allow developers to use ``config.include('pyramid_alchemy')`` to register
  the ``add_model_method`` configuration directive.
"""

from .directive import add_model_method

def includeme(config):
    config.add_directive('add_model_method', add_model_method)

