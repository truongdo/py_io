#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 truong-d <truong-d@truongd-XPS13-9333>
#
# Distributed under terms of the MIT license.

"""

"""

from collections import OrderedDict
import logging
import sys
import subprocess
import py_log

logger = logging.getLogger(__name__)


def read_from_pipe(fn):
    """ Read from pipeline """
    proc = subprocess.Popen(fn.strip().split(), stdout=subprocess.PIPE)
    output = proc.stdout.read()
    return output.strip().split("\n")


def read_any(fn):
    """ Read data from any input
    :fn: can be a file, filename, or even pipeline.
    :returns: list of data

    Examples:
    >>> read_any("cat file.scp|")
    >>> read_any("file.scp")
    """

    fn = fn.strip()
    if "|" in fn[-1]:
        fn = fn.strip("|")
        data = read_from_pipe(fn)
    else:
        data = open(fn, 'r').readlines()

    return data


def read_scp(istream):
    """Read table format from istream

    :istream: file descripter or filename.
    :allow_dup: allow duplication keys, values will become a list
    :returns: OrderedDict object

    Examples
    >>> read_scp("file.scp")
    >>> read_scp("cat file.scp|")
    """

    if isinstance(istream, file):
        istream = istream.name

    data = OrderedDict()
    for line in read_any(istream):
        ps = line.strip().split()

        if ps[0] in data:
            logger.error("Got duplicated keys: %s in %s", ps[0], istream.name)
            exit(1)

        data[ps[0]] = " ".join(ps[1:])

    return data


def write_scp(data, ostream):
    """Write table format to ostream

    :data: Dictionary type data
    :ostream: file descripter or filename or - for stdout. If filename, then convert to file descriptor

    Examples:
        >>> write_scp({"a": 1, "b":2}, sys.stdout)
    """

    if not isinstance(ostream, file) and ostream != "-":
        ostream = open(ostream, 'w')
    elif ostream == "-":
        ostream = sys.stdout

    if not isinstance(data, dict):
        logger.error("Got non-dictionary data type")
        exit(1)

    text = []
    for key, value in data.items():
        text.append("%s %s" % (key, str(value)))
    ostream.write("\n".join(text))


def read_input(fn):
    """ Read input. Supports to read from file or pipeline

    :input: string type. Format would be \"scp:scp_file\", or \"file_name\", or \"cat file_name|\"
    :returns: dictionary in case of scp, and list in case of normal file

    If
        :input: scp:scp_file, we will read as scp file
        :input: filename, we will read as normal file

    """

    if "scp:" in fn:
        string = fn.split(":")[-1]
        data = read_scp(string)
        return data
    else:
        return read_any(fn)


def write_output(data, ostream=None):
    """ Read input. Supports to read from file or pipeline

    :input: string type. Format would be \"scp:scp_file\", or \"file_name\", or \"cat file_name|\"
    :returns: dictionary in case of scp, and list in case of normal file

    If
        :input: scp:scp_file, we will read as scp file
        :input: filename, we will read as normal file

    """

    if isinstance(ostream, file):
        ostream = ostream.name

    if ostream and ("scp:" in ostream):
        string = ostream.split(":")[-1]
        write_scp(data, string)
    else:
        data_to_write = None
        if isinstance(data, dict):
            data_to_write = data.values()
        else:
            data_to_write = data

        string = []
        for d in data_to_write:
            string.append(str(d))

        if not ostream or (ostream in ["<stdout>", "-"]):
            sys.stdout.write("\n".join(string))
        else:
            open(ostream, 'w').write("\n".join(string))

if __name__ == '__main__':
    data = read_scp("cat examples/read_scp.txt|")
    data = read_scp("examples/read_scp.txt")
    write_scp(data, sys.stdout)
