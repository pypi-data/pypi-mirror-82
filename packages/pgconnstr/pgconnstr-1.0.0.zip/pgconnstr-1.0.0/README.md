pgconnstr
=========

A Python module for parsing and manipulating PostgreSQL libpq style connection strings and URIs.

[![PyPI version](https://badge.fury.io/py/pgconnstr.svg)](https://badge.fury.io/py/pgconnstr)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pgconnstr.svg)](https://pypi.python.org/pypi/pgconnstr/)
[![GitHub license](https://img.shields.io/github/license/canonical/pgconnstr)](https://github.com/canonical/pgconnstr/blob/master/LICENSE)
[![GitHub Actions (Tests)](https://github.com/canonical/pgconnstr/workflows/Tests/badge.svg)](https://github.com/canonical/pgconnstr/actions?query=workflow%3ATests)


License
-------

LGPLv3. See the file `LICENSE` for details.

class ConnectionString
----------------------

pgconnstr.ConnectionString represents a libpq connection string.

```python console
>>> from pgconnstr import ConnectionString
>>> c = ConnectionString(host='1.2.3.4', dbname='mydb', port=5432, user='anon',
...                      password="sec'ret", application_name='myapp')
...
>>> print(str(c))
application_name=myapp dbname=mydb host=1.2.3.4 password=sec\'ret port=5432 user=anon
>>> print(str(ConnectionString(str(c), dbname='otherdb')))
application_name=myapp dbname=otherdb host=1.2.3.4 password=sec\'ret port=5432 user=anon

```

Components may be accessed as attributes.

```python console
>>> c.dbname
'mydb'
>>> c.host
'1.2.3.4'
>>> c.port
'5432'

```

Standard components will default to None if not explicitly set. See
https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-PARAMKEYWORDS
for the list of standard keywords.

```python console
>>> c.connect_timeout is None
True

```

The standard URI format is also accessible:

```python console
>>> print(c.uri)
postgresql://anon:sec%27ret@1.2.3.4:5432/mydb?application_name=myapp

>>> print(ConnectionString(c, host='2001:db8::1234').uri)
postgresql://anon:sec%27ret@[2001:db8::1234]:5432/mydb?application_name=myapp

```
