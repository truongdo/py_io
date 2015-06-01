#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 truong-d <truong-d@truongd-XPS13-9333>
#
# Distributed under terms of the MIT license.

"""

"""

from py_io import read_input, write_output
import sys

if __name__ == '__main__':
    data = read_input("grep \"import read_input\" main.py|")
    print data
    # write_output(data, sys.argv[2])
