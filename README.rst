=====================
BrainFrame Python API
=====================

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


Installation
------------

The BrainFrame Python API is available on PyPI and can be installed with pip.
Install the version of the library that matches the version of BrainFrame that
you are using.

.. code-block:: bash

   pip3 install brainframe-api==0.26.0
