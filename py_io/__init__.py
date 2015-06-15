#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 truong-d <truong-d@truongd-XPS13-9333>
#
# Distributed under terms of the MIT license.

"""

"""

import logging
import logging.config
import Colorer
from collections import OrderedDict
import sys
import subprocess
import shlex
import optparse

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
})


logger = logging.getLogger(__name__)


def read_from_pipe(fn):
    """ Read from pipeline """
    cmd = fn
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    output = proc.stdout.read()
    return output.strip()


def read_any(fn):
    """ Read data from any input
    :fn: can be a file, filename, or even pipeline.
    :returns: data of fn (string)

    Examples:
    >>> read_any("cat file.scp|")
    >>> read_any("file.scp")
    """

    if "stdin" in fn:
        return sys.stdin.read()

    fn = fn.strip()
    if "|" in fn[-1]:
        fn = fn.strip("|")
        data = read_from_pipe(fn)
    else:
        data = open(fn, 'r').read()

    return data


def read_scp(istream, sep=None, allow_dup=False):
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
    for line in read_any(istream).strip().split("\n"):
        ps = line.strip().split()
        if not ps:
            continue
        if ps[0] in data and (not allow_dup):
            logger.error("Got duplicated keys: %s in %s", ps[0], istream)
            exit(1)

        text = " ".join(ps[1:])
        if sep:
            if ps[0] in data and allow_dup:
                data[ps[0]].append(text.split(sep))
            else:
                if allow_dup:
                    data[ps[0]] = [text.split(sep)]
                else:
                    data[ps[0]] = text.split(sep)
        else:
            if ps[0] in data and allow_dup:
                data[ps[0]].append(text)
            else:
                if allow_dup:
                    data[ps[0]] = [text]
                else:
                    data[ps[0]] = text

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


def read_input(fn, sep=None, allow_dup=False):
    """ Read input. Supports to read from file or pipeline

    :input: string type. Format would be \"scp:scp_file\", or \"file_name\", or \"cat file_name|\"
    :allow_dup: binary. Only use when the input is scp type
    :returns: dictionary in case of scp, and list in case of normal file

    If
        :input: scp:scp_file, we will read as scp file
        :input: filename, we will read as normal file

    """

    if type(fn) is file:
        return fn.read().strip().split("\n")

    if "scp:" in fn:
        string = fn[4:]  # Skip scp
        data = read_scp(string, sep=sep, allow_dup=allow_dup)
        return data
    else:
        return read_any(fn).strip()   # Do not split, load HMMSet.read need the whole data


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


def easy_option(arg_list):
    """ Easily parse options, and arguments function

    Arguments:
    ---------------------
        arg_list: (list) list of arguments you want to parse

    Returns:
    ---------------------
        opts, args

    Examples:
    >>> import py_io
    >>> py_io.easy_option(["opt1", "opts2"])
    """
    parser = optparse.OptionParser()
    for arg in arg_list:
        parser.add_option("--" + arg)
    opts, args = parser.parse_args()
    return opts, args


if __name__ == '__main__':
    #data = read_scp("cat examples/read_scp.txt|")
    #data = read_scp("examples/read_scp.txt")
    #write_scp(data, sys.stdout)
    #print easy_option(["opt1"])
    print read_scp("scp:sys.stdin", sep=" ")
