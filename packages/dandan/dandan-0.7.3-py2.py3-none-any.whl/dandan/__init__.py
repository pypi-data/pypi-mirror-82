"""
**dandan package**

Several convenient tools for python programming


**Events**

- 2020-10-10 [0.7.3] remove psutil in dependencies
- 2018-10-13 [0.7.2] fix bug for AttrDict call dict.update
- 2018-10-11 [0.7.1] optimize performance for AttrDict and fix bug
- 2018-10-11 [0.7.0] optimize performance for AttrDict
- 2018-05-21 [0.6.0] add interrupt decorator
- 2018-05-16 [0.5.8] fix bug for AttrDict member functions
- 2018-05-12 [0.5.7] improve code robustness
- 2018-05-11 [0.5.6] modify logger roll suffix is "%Y-%m-%d.log"
- 2018-05-07 [0.5.5] fix bug for md5 and sha1
- 2018-05-03 [0.5.4] fix bug for logger file utf8 encoding
- 2018-04-28 [0.5.3] fix bug for logger file
- 2018-03-23 [0.5.2] add default logger name as 'dandan'
- 2017-12-13 [0.5.1] fix bug
- 2017-12-13 [0.5.0] add system.kill and execute timeout
- 2017-12-12 [0.4.2] fix bug for system.execute in callback mode
- 2017-12-11 [0.4.1] fix bug for system.execute return result with str
- 2017-12-10 [0.4.0] add getLogger method in logger
- 2017-11-29 [0.3.3] fix bug for put_json in python3
- 2017-11-29 [0.3.2] add indent for dandan.value.put_json
- 2017-11-19 [0.3.1] fix bug in dandan.value.length when given string length is zero
- 2017-11-19 [0.3.0] add function dandan.value.length
- 2017-11-17 [0.2.3] update document for project enhance AttrDict class
- 2017-11-15 [0.2.2] update document for project
- 2017-10-14 move to another github project
- 2017-06-25 add function system.clear
- 2017-06-23 add function system.getch
- 2017-06-23 Support python3
- 2017-06-23 Add TestCase
"""

from __future__ import absolute_import

from dandan import error
from dandan import query
from dandan import system
from dandan import traffic
from dandan import value
from dandan import utils
from dandan import logger

__all__ = [
    "error",
    "query",
    "system",
    "traffic",
    "value",
    "utils",
    "logger"
]

__version__ = ".".join(
    [str(var) for var in
        [
            0,
            7,
            3
    ]
    ])
