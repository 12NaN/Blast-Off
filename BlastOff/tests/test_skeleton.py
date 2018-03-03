#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from blastoff.skeleton import fib

__author__ = "[12NaN]"
__copyright__ = "[12NaN]"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
