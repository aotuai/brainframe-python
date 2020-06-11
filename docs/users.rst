Users
=====

A single BrainFrame server can have multiple users associated with it. Each
user has their own username and password, and can be assigned roles that grant
them different levels of access to the server.

Note that authorization is disabled by default for BrainFrame servers. See
the `Authorization Configuration`_ section in the User Manual for details.

API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_user

.. automethod:: brainframe.api.BrainFrameAPI.get_users

.. automethod:: brainframe.api.BrainFrameAPI.set_user

.. automethod:: brainframe.api.BrainFrameAPI.delete_user

Data Structures
---------------

.. automodule:: brainframe.api.bf_codecs.user_codecs
   :members:

.. _`Authorization Configuration`:
   https://aotu.ai/docs/advanced_usage/server_configuration/#authorization-configuration
