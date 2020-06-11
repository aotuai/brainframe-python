Alarms
======

Alarms allow BrainFrame to notify you when a specified condition happens within
a zone. When the conditions for an alarm are met, the alarm generates alerts
which contain the time at which the conditions occurred as well as a frame from
the video at that time. See the `Alarms`_ section in the User Manual for
details.

API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_zone_alarm

.. automethod:: brainframe.api.BrainFrameAPI.get_zone_alarms

.. automethod:: brainframe.api.BrainFrameAPI.set_zone_alarm

.. automethod:: brainframe.api.BrainFrameAPI.delete_zone_alarm

.. automethod:: brainframe.api.BrainFrameAPI.get_alert

.. automethod:: brainframe.api.BrainFrameAPI.get_alerts

.. automethod:: brainframe.api.BrainFrameAPI.set_alert_verification

.. automethod:: brainframe.api.BrainFrameAPI.get_alert_frame

Data Structures
---------------

.. automodule:: brainframe.api.bf_codecs.alarm_codecs
   :members:

.. automodule:: brainframe.api.bf_codecs.condition_codecs
   :members:

.. _`Alarms`:
   https://aotu.ai/docs/user_guide/alarms/
