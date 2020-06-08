Identities
==========

Identities are known specific instances of an object that can be later
recognized. For example, a picture of a person's face can be encoded and
associated with that person's identity so that they can be recognized when
they're in a video stream.

Identities can also be associated with vectors directly in cases where the
encoding of an object is known ahead-of-time, like in the case of a fiducial
tag.

.. code-block:: python

   """Creates an identity for a specific skew of car using a picture of that
   car.
   """
   from pathlib import Path

   from brainframe.api import BrainFrameAPI
   from brainframe.bf_codecs import Identity

   api = BrainFrameAPI("http://localhost")

   civic_image_bytes = Path("civic.jpg").read_bytes()
   # Upload the image to the server
   storage_id = api.new_storage(civic_image_bytes, "image/jpeg")

   # Create the new identity for the car skew
   identity = api.set_identity(Identity(
       unique_name="g10-R16B-blue-sedan",
       nickname="Honda Civic 2018 Blue Sedan",
   ))
   # Encode an image of the skew and associate that encoding with the identity
   api.new_identity_image(identity.id, "car", storage_id)


API Methods
-----------

.. automethod:: brainframe.api.BrainFrameAPI.get_identity

.. automethod:: brainframe.api.BrainFrameAPI.get_identities

.. automethod:: brainframe.api.BrainFrameAPI.set_identity

.. automethod:: brainframe.api.BrainFrameAPI.delete_identity

.. automethod:: brainframe.api.BrainFrameAPI.new_identity_image

.. automethod:: brainframe.api.BrainFrameAPI.new_identity_vector

.. automethod:: brainframe.api.BrainFrameAPI.get_encoding

.. automethod:: brainframe.api.BrainFrameAPI.get_encodings

.. automethod:: brainframe.api.BrainFrameAPI.get_encoding_class_names

.. automethod:: brainframe.api.BrainFrameAPI.delete_encoding

.. automethod:: brainframe.api.BrainFrameAPI.delete_encodings

Data Structures
---------------

.. automodule:: brainframe.api.bf_codecs.identity_codecs
   :members:
