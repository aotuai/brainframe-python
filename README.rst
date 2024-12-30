BrainFrame Python API
=====================

.. image:: https://readthedocs.org/projects/brainframe-python-api/badge/?version=latest
   :target: https://brainframe-python-api.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://circleci.com/gh/aotuai/brainframe-python.svg?style=svg
   :target: https://circleci.com/gh/aotuai/brainframe-python
   :alt: Publish Packages CI Status

This library is a Python wrapper around the BrainFrame REST API. It allows for
easy interaction with a BrainFrame server.

.. code-block:: python

   from brainframe.api import BrainFrameAPI, bf_codecs

   # Connect to the server
   api = BrainFrameAPI("http://localhost")

   # Create a new IP camera stream
   stream_config = api.set_stream_configuration(
       bf_codecs.StreamConfiguration(
           name="New Stream",
           connection_type=bf_codecs.ConnType.IP_CAMERA,
           connection_options={"url": "rtsp://192.168.1.100"},
           runtime_options={},
       ))
   api.start_analyzing(stream_config.id)

   # Get results
   analysis_results = api.get_latest_zone_statuses()

# Build brainframe-api wheel

.. code-block:: bash

   poetry build

The output will be in dist/. Check the README format if it is updated,

.. code-block:: bash

   pip install readme-renderer
   python -m readme_renderer README.rst

Installation
============

The BrainFrame Python API is available on PyPI and can be installed with pip.
Install the version of the library that matches the version of BrainFrame that
you are using.

.. code-block:: bash

   pip3 install brainframe-api

Or local build,

.. code-block:: bash

   pip3 install dist/{file name.whl}

Documentation
=============

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme
   cd docs
   make html

Read the generated docs,

.. code-block:: bash

   firefox _build/html/index.html

Documentation for this library is available on `ReadTheDocs`_.

.. _`ReadTheDocs`:
   https://brainframe-python-api.readthedocs.io/en/latest/

