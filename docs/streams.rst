Streams
=======

BrainFrame works by connecting to and running analysis on video streams.
Streams can come from a variety of sources and have analysis be turned on or
off at runtime.

Below is an example script that uploads a video file, starts streaming it, and
turns on analysis for that stream.

.. code-block:: python

   from pathlib import Path

   from brainframe.api import BrainFrameAPI
   from brainframe.api.bf_codecs import StreamConfiguration, ConnType

   api = BrainFrameAPI("http://localhost")

   video_bytes = Path("video_file.mp4").read_bytes()
   storage_id = api.new_storage(video_bytes, "video/mp4")

   stream_config = api.set_stream_configuration(
       StreamConfiguration(
           name="My Video File",
           connection_type=ConnType.FILE,
           connection_options={"storage_id": storage_id},
           runtime_options={},
       ))
 
   api.start_analyzing(stream_config.id)

API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_stream_configuration

.. automethod:: brainframe.api.BrainFrameAPI.get_stream_configurations

.. automethod:: brainframe.api.BrainFrameAPI.set_stream_configuration

.. automethod:: brainframe.api.BrainFrameAPI.start_analyzing

.. automethod:: brainframe.api.BrainFrameAPI.stop_analyzing

.. automethod:: brainframe.api.BrainFrameAPI.delete_stream_configuration

.. automethod:: brainframe.api.BrainFrameAPI.get_stream_url

.. automethod:: brainframe.api.BrainFrameAPI.get_runtime_options

.. automethod:: brainframe.api.BrainFrameAPI.set_runtime_option_vals


Data Structures
---------------

.. automodule:: brainframe.api.bf_codecs.config_codecs
   :members:
