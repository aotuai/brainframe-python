Storage
=======

The BrainFrame server has a generic API for file storage that is used by other
API endpoints. If a method asks for a ``storage_id`` field, it's looking for a
file uploaded using these methods.

API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_storage_data

.. automethod:: brainframe.api.BrainFrameAPI.get_storage_data_as_image

.. automethod:: brainframe.api.BrainFrameAPI.new_storage

.. automethod:: brainframe.api.BrainFrameAPI.new_storage_as_image

.. automethod:: brainframe.api.BrainFrameAPI.delete_storage
