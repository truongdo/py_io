# Introductions #
This is a small library for python that allows to perform IO operations more easily.

Let's see some examples to show how to use it. It is very simple!

# Installation #
```
pip install git+https://github.com/truongdq/py_io.git
```

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
>>> text = py_io.read_input("scp:text.scp", sep=" ")
>>> print text
>>> {'fileid1': ['hello'], 'fileid2': ['I'm', 'sleeply']}
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

## Writing ##
Writing in py_io is just as simple as reading.

```
py_io.write("hello", "-")  # Write to stdout
py_io.write("hello", "output.txt")
py_io.write("hello", "|cat -")
```

Write data one by one
```
writer = py_io.get_writer("output.txt")
writer.write("hello world")
writer.write("how are you?")
writer.close()

# It is a bit complex when write to pipe
proc = py_io.get_writer("|cat -")
writer = proc.stdin
writer.write("hello word")
stdout, stderr = proc.communicate()
```

Noted that when using read or write with pipe, it is necessary to escape the special characters.
For examples,

```
py_io.write("hello", "|sed \"s/el/go/g\"")
```

