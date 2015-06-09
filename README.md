# Introductions #
This is a small library for python that allows to perform IO operations more easily.

Please see the examples below for how to use the library. It is very simple!

# Examples #
## Reading from scp file ##
Assume you have the text.scp in the following format:
```
> cat text.scp
fileid1 hello
fileid2 I'm sleeply
```


```
>>> import py_io
>>> import py_io.py_log    # Just for logging
>>> text = py_io.read_input("scp:text.scp")
>>> print text
>>> {'fileid1': 'hello', 'fileid2': 'I'm sleeply'}
```

## Reading from pipe (Linux) ##
```
>>> print py_io.read_input("cat text.scp|")
>>> "fileid1 hello\n fileid2 I'm sleeply"
```

``py_io.read_input`` automatically detect if it needs to read from pipe if the character __|__ appear
at the end of its argument.

You can even write a command like below,
```
>>> py_io.read_input("cat text.scp |  head -n 10 |")
```
