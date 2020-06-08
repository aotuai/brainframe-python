Analysis Results
================

The BrainFrame server organizes detected objects by the zones that those
detections were found in. Detections for a zone, alongside information on that
zone's state and any active alerts for that zone, are contained in ZoneStatus
objects. For every video frame where analysis is performed, a ZoneStatus
object will be created for every zone in that frame.

API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_latest_zone_statuses

.. automethod:: brainframe.api.BrainFrameAPI.get_zone_status_stream

Data Structures
---------------

.. autoclass:: brainframe.api.bf_codecs.zone_codecs.ZoneStatus
   :members:
