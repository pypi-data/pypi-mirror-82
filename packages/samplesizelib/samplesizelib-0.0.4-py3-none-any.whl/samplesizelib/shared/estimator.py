#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The :mod:`samplesizelib.shared.estimator` contains classes:
- :class:`samplesizelib.shared.estimator.SampleSizeEstimator`
"""
from __future__ import print_function

__docformat__ = 'restructuredtext'

from tqdm import tqdm

class SampleSizeEstimator(object):
    r"""Base class for all sample size estimation models."""

    def __init__(self):
        r"""Constructor method
        """
        self._percentage_of_completion_status = 0.

    def status(self):
        r"""
        Returns the percentage of completion.
        
        :return: percentage of completion.
        :rtype: float
        """
        return self._percentage_of_completion_status

    def _set_status(self, new_percentage):
        r"""
        change percentage of completion status
        """
        new_percentage = float(new_percentage)
        if 0 <= new_percentage <= 100:
            self._percentage_of_completion_status = new_percentage

    def _progressbar(self, iterable):
        r"""
        Init tqdm progressbar
        """
        iterator = tqdm(iterable)
        iterator.set_description_str(self.__class__.__name__)
        return iterator

    def __call__(self, features, target):
        r"""
        Returns sample size prediction for the given dataset.
        
        :param features: The tensor of shape
            `num_elements` :math:`\times` `num_feature`.
        :type features: array.
        :param target: The tensor of shape `num_elements`.
        :type target: array.
        
        :return: sample size estimation for the given dataset.
        :rtype: float
        """
        return self.forward(features, target)

    def forward(self, features, target):
        r"""
        Returns sample size prediction for the given dataset.
        
        :param features: The tensor of shape
            `num_elements` :math:`\times` `num_feature`.
        :type features: array.
        :param target: The tensor of shape `num_elements`.
        :type target: array.
        
        :return: sample size estimation for the given dataset.
        :rtype: float
        """
        raise NotImplementedError