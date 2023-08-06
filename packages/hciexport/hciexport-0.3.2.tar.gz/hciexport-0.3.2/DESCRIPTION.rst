HCI export
==========

The **hciexport** tool facilitates the APIs provided by
*Hitachi Content Intelligenc* (HCI) to export Workflow bundles
and System configuration packages.

The functionality as such is also available through the HCI GUIs,
but sometimes, one want to be able to export them as part of an
automated task (backup), where using the APIs is more appropriate.

Features

    *   Export a complete Workflow bundle
    *   Export the complete System configuration

Dependencies
------------

You need to have at least Python 3.7 installed to run **hciexport**.

It depends on the `httpx <https://www.python-httpx.org>`_ for
communication with HCI.

Documentation
-------------

To be found at `readthedocs.org <http://hciexport.readthedocs.org>`_

Installation
------------

Install **hciexport** by running::

    $ pip install hciexport


-or-

get the source from `gitlab.com <https://gitlab.com/simont3/hciexport>`_,
unzip and run::

    $ python setup.py install


-or-

Fork at `gitlab.com <https://gitlab.com/simont3/hciexport>`_

Contribute
----------

- Source Code: `<https://gitlab.com/simont3/hciexport>`_
- Issue tracker: `<https://gitlab.com/simont3/hciexport/issues>`_

Support
-------

If you've found any bugs, please let me know via the Issue Tracker;
if you have comments or suggestions, send an email to `<sw@snomis.eu>`_

License
-------

The MIT License (MIT)

Copyright (c) 2020 Thorsten Simons (sw@snomis.eu)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
