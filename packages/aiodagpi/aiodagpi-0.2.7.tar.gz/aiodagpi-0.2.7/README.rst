aiodagpi
========

.. image:: https://travis-ci.com/DevilJamJar/aiodagpi.svg?branch=master
    :target: https://travis-ci.com/DevilJamJar/aiodagpi
    :alt: Latest Travis build status

.. image:: https://img.shields.io/pypi/v/aiodagpi.svg
    :target: https://pypi.python.org/pypi/aiodagpi
    :alt: Latest PyPI version

.. image:: https://img.shields.io/badge/license-MIT-yellowgreen
    :target: https://mit-license.org
    :alt: MIT License link

.. image:: https://img.shields.io/badge/api-dagpi-yellow
    :target: https://dagpi.tk
    :alt: Dagpi.tk link

.. image:: https://img.shields.io/badge/python-3.6%2B-blue
    :target: https://www.python.org/downloads/
    :alt: Python version 3.6 and above

An asynchronous python API wrapper for Dagpi : https://dagpi.tk

Installation
------------
Install via pip, either directly from PyPI:

.. code:: sh

    >>> python3 -m pip install -U aiodagpi

or from the github repository:

.. code:: sh

    >>> python3 -m pip install -U git+https://github.com/DevilJamJar/aiodagpi

Alternatively, download files directly from `download files <https://pypi.org/project/aiodagpi/#files>`_. This is not recommended and can cause directory issues later down the line if not placed and constructed correctly. If you must, use `this guide <https://packaging.python.org/tutorials/installing-packages/>`_ for help on how to install python packages.

Usage
-----

Creating the client instance with your dagpi token:

.. code:: py

    from aiodagpi import aiodagpiclient
    dagpi = aiodagpiclient('Dagpi Token')

Examples
--------

Deepfrying an image:

.. code:: py

    async def deepfry(url:str):
        image = await dagpi.animated('deepfry', url)
        return image

Output:

.. code:: py

    {'success': True, 'url': 'http://dagpi.tk/bin/nKuT5rD0dj.gif'}

A full options list can be found in the docstring for each client method. or by using:

.. code:: py

    print(dagpi.get.__doc__)

Output:

.. code:: py

    Perform a GET request for one of the specified options

        Args:
            option (str): The option, possibles:
            
            'wtp', 'logogame'

        Raises:
            InvalidOption: Invalid option provided

        Returns:
            dict: The dictionary response to the GET request

Authors
-------

`aiodagpi` was written by `Raj Sharma <yrsharma@icloud.com>`_.

`dagpi.tk` was constructed by `Daggy1234 <https://github.com/Daggy1234>`_.
