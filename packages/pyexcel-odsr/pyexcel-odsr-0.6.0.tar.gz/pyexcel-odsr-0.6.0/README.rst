================================================================================
pyexcel-odsr - Let you focus on data, instead of ods format
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/chfw

.. image:: https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg
   :target: https://awesome-python.com/#specific-formats-processing

.. image:: https://travis-ci.org/pyexcel/pyexcel-odsr.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-odsr

.. image:: https://codecov.io/gh/pyexcel/pyexcel-odsr/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel-odsr

.. image:: https://badge.fury.io/py/pyexcel-odsr.svg
   :target: https://pypi.org/project/pyexcel-odsr


.. image:: https://pepy.tech/badge/pyexcel-odsr/month
   :target: https://pepy.tech/project/pyexcel-odsr/month


.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby

.. image:: https://img.shields.io/static/v1?label=continuous%20templating&message=%E6%A8%A1%E7%89%88%E6%9B%B4%E6%96%B0&color=blue&style=flat-square
    :target: https://moban.readthedocs.io/en/latest/#at-scale-continous-templating-for-open-source-projects

.. image:: https://img.shields.io/static/v1?label=coding%20style&message=black&color=black&style=flat-square
    :target: https://github.com/psf/black

**pyexcel-odsr** is a specialized ods reader based on tailored ods reader from
`messytables <https://github.com/okfn/messytables>`_.
You are likely to use it with `pyexcel <https://github.com/pyexcel/pyexcel>`_.
Differring from `pyexcel-ods <https://github.com/pyexcel/pyexcel-ods>`_ and
`pyexcel-ods3 <https://github.com/pyexcel/pyexcel-ods3>`_ in handling ods file, this
library could read partial content from a huge ods file.


Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please support me on github, `patreon <https://www.patreon.com/bePatron?u=5537627>`_
or `bounty source <https://salt.bountysource.com/teams/chfw-pyexcel>`_ to maintain
the project and develop it further.

If you are an individual, you are welcome to support me too and for however long
you feel like. As my backer, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

And your issues will get prioritized if you would like to become my patreon as `pyexcel pro user`.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.


Known constraints
==================

Fonts, colors and charts are not supported.

Installation
================================================================================


You can install pyexcel-odsr via pip:

.. code-block:: bash

    $ pip install pyexcel-odsr


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel-odsr.git
    $ cd pyexcel-odsr
    $ python setup.py install

Usage
================================================================================

As a standalone library
--------------------------------------------------------------------------------

.. testcode::
   :hide:

    >>> import os
    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import BytesIO as StringIO
    >>> PY2 = sys.version_info[0] == 2
    >>> if PY2 and sys.version_info[1] < 7:
    ...      from ordereddict import OrderedDict
    ... else:
    ...     from collections import OrderedDict


.. testcode::
   :hide:

    >>> from pyexcel_ods import save_data
    >>> data = OrderedDict() # from collections import OrderedDict
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
    >>> save_data("your_file.ods", data)


Read from an ods file
********************************************************************************

Here's the sample code:

.. code-block:: python

    >>> from pyexcel_odsr import get_data
    >>> data = get_data("your_file.ods")
    >>> import json
    >>> print(json.dumps(data))
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [["row 1", "row 2", "row 3"]]}



.. testcode::
   :hide:

    >>> data = OrderedDict()
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [[7, 8, 9], [10, 11, 12]]})
    >>> io = StringIO()
    >>> save_data(io, data)
    >>> unused = io.seek(0)
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading




Read from an ods from memory
********************************************************************************

Continue from previous example:

.. code-block:: python

    >>> # This is just an illustration
    >>> # In reality, you might deal with ods file upload
    >>> # where you will read from requests.FILES['YOUR_ODS_FILE']
    >>> data = get_data(io)
    >>> print(json.dumps(data))
    {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [[7, 8, 9], [10, 11, 12]]}


Pagination feature
********************************************************************************



Let's assume the following file is a huge ods file:

.. code-block:: python

   >>> huge_data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33],
   ...     [4, 24, 34],
   ...     [5, 25, 35],
   ...     [6, 26, 36]
   ... ]
   >>> sheetx = {
   ...     "huge": huge_data
   ... }
   >>> save_data("huge_file.ods", sheetx)

And let's pretend to read partial data:

.. code-block:: python

   >>> partial_data = get_data("huge_file.ods", start_row=2, row_limit=3)
   >>> print(json.dumps(partial_data))
   {"huge": [[3, 23, 33], [4, 24, 34], [5, 25, 35]]}

And you could as well do the same for columns:

.. code-block:: python

   >>> partial_data = get_data("huge_file.ods", start_column=1, column_limit=2)
   >>> print(json.dumps(partial_data))
   {"huge": [[21, 31], [22, 32], [23, 33], [24, 34], [25, 35], [26, 36]]}

Obvious, you could do both at the same time:

.. code-block:: python

   >>> partial_data = get_data("huge_file.ods",
   ...     start_row=2, row_limit=3,
   ...     start_column=1, column_limit=2)
   >>> print(json.dumps(partial_data))
   {"huge": [[23, 33], [24, 34], [25, 35]]}

.. testcode::
   :hide:

   >>> os.unlink("huge_file.ods")


As a pyexcel plugin
--------------------------------------------------------------------------------

No longer, explicit import is needed since pyexcel version 0.2.2. Instead,
this library is auto-loaded. So if you want to read data in ods format,
installing it is enough.


Reading from an ods file
********************************************************************************

Here is the sample code:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_book(file_name="your_file.ods")
    >>> sheet
    Sheet 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet 2:
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+



.. testcode::
   :hide:

    >>> sheet.save_as("another_file.ods")



Reading from a IO instance
********************************************************************************

You got to wrap the binary content with stream to get ods working:

.. code-block:: python

    >>> # This is just an illustration
    >>> # In reality, you might deal with ods file upload
    >>> # where you will read from requests.FILES['YOUR_ODS_FILE']
    >>> odsfile = "another_file.ods"
    >>> with open(odsfile, "rb") as f:
    ...     content = f.read()
    ...     r = pe.get_book(file_type="ods", file_content=content)
    ...     print(r)
    ...
    Sheet 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet 2:
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+




License
================================================================================

New BSD License

Developer guide
==================

Development steps for code changes

#. git clone https://github.com/pyexcel/pyexcel-odsr.git
#. cd pyexcel-odsr

Upgrade your setup tools and pip. They are needed for development and testing only:

#. pip install --upgrade setuptools pip

Then install relevant development requirements:

#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt

Once you have finished your changes, please provide test case(s), relevant documentation
and update CHANGELOG.rst.

.. note::

    As to rnd_requirements.txt, usually, it is created when a dependent
    library is not released. Once the dependecy is installed
    (will be released), the future
    version of the dependency in the requirements.txt will be valid.


How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make

On Windows systems, please issue this command::

    > test.bat


Before you commit
------------------------------

Please run::

    $ make format

so as to beautify your code otherwise travis-ci may fail your unit test.


Credits
================================================================================

This library is based on the ods of messytables, Open Knowledge Foundation Ltd.


.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.ods")
   >>> os.unlink("another_file.ods")
