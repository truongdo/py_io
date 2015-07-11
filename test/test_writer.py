#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 truong-d <truong-d@truongd-XPS13-9333>
#
# Distributed under terms of the MIT license.

"""

"""
import sys
import unittest
import py_io
from StringIO import StringIO


class TestPyIO(unittest.TestCase):

    def test_write_to_file(self):
        py_io.write_to_file("this is not good", open("out.txt", "w"))
        txt = py_io.read_input("out.txt")
        self.assertEqual(txt, "this is not good")

    def test_write_to_file2(self):
        py_io.write_to_file("this is not good", "out.txt")
        txt = py_io.read_input("out.txt")
        assert txt == "this is not good"

    def test_write_to_file_empty(self):
        py_io.write_to_file("", "out.txt")
        txt = py_io.read_input("out.txt")
        assert txt == ""

    def test_write_to_pipe(self):
        py_io.write_to_pipe("hello how are you", "sed \"s/hello/abc/g\" > abc")
        output = open("abc").read()
        self.assertEqual("abc how are you", output)

    def test_write_stdout(self):

        py_io.write("output", open("abc", "wb"))
        output = open("abc").readline().strip()
        self.assertEqual("output", output)

        py_io.write("output", "abc")
        output = open("abc").readline().strip()
        self.assertEqual("output", output)

        py_io.write("output", "|sed \"s/out/replace/g\" > abc")
        output = open("abc").readline().strip()
        self.assertEqual("replaceput", output)

    def test_get_writer(self):
        writer = py_io.get_writer("abc")
        self.assertIsInstance(writer, file)

        writer = py_io.get_writer("sys.stdout")
        self.assertIsInstance(writer, file)

        proc = py_io.get_writer("|sed \"s/out/mmm/g\" > abc")
        writer = proc.stdin
        self.assertIsInstance(writer, file)
        writer.write("output1\n")
        writer.write("output2")
        proc.communicate()
        output = open("abc").read()
        self.assertEqual("mmmput1\nmmmput2", output)


if __name__ == '__main__':
    unittest.main()
