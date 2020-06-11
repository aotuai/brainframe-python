The BrainFrameAPI Class
=======================

The ``BrainFrameAPI`` class holds methods corresponding to all API endpoints
that the server provides. In order to get connected to a BrainFrame server,
start by initializing a new instance of this class.

.. code-block:: python

   from brainframe.api import BrainFrameAPI

   # Log into a local BrainFrame server instance with the default admin
   # credentials
   api = BrainFrameAPI("http://localhost", ("admin", "admin"))

Take a look at the next few topics for information on all the methods the
``BrainFrameAPI`` class has available and their corresponding data structures.

Basic Methods
-------------

.. autoclass:: brainframe.api.BrainFrameAPI
   :members:
