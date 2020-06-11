Premises
========

By default, the BrainFrame server connects to IP cameras directly. This
necessitates that the the IP camera is either on the same network as the
server, or is made accessible through other means, like port forwarding.

For situations where this is undesirable, a stream may optionally be configured
to be part of a premises. BrainFrame will connect to these streams through the
StreamGateway instead, which acts as a proxy to bypass firewalls. See the
`Premises`_ section in the User Manual for details.

API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_premises

.. automethod:: brainframe.api.BrainFrameAPI.get_all_premises

.. automethod:: brainframe.api.BrainFrameAPI.set_premises

.. automethod:: brainframe.api.BrainFrameAPI.delete_premises

Data Structures
---------------

.. automodule:: brainframe.api.bf_codecs.premises_codecs
   :members:

.. _`Premises`:
   https://aotu.ai/docs/user_guide/premises/
