.. highlight:: shell

============
Installation
============

.. warning::

    We use the pyqtgraph library which contains an `issue with venv on Windows`_. Windows users should see the linked
    issue for details and prefer `virtualenv` over `python -m venv`.

.. _issue with venv on Windows: https://github.com/pyqtgraph/pyqtgraph/issues/1052

Stable release
--------------

To install Quantify, run this command in your terminal:

.. code-block:: console

    $ pip install Quantify-core

This is the preferred method to install Quantify, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Quantify can be downloaded from the `GitLab repo`_:

.. code-block:: console

    $ git clone https://gitlab.com/Quantify-os/Quantify-core.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .

If you are a developer you might want to install the package in the editable mode:

.. code-block:: console

    $ pip install -e .

.. _GitLab repo: https://gitlab.com/Quantify-os/Quantify-core

PyQt5
------

Quantify-core has a dependency on the PyQt5 package, which itself has a dependency on the Qt5 runtime. On most systems,
the standard installation process will install Qt. You may need to consult a search engine if you have a more exotic
system.
