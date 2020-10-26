MongoDB Handler
***************

This handler save the measured energy sample on a mongoDB database

How to Use it
-------------

Create a ``MongoHandler`` instance and pass it as a parameter of the context manager or the function decorator. You have to specify the uri of the database, the database and the collection name.

When the measure is done, you have to use the ``save_data`` method to store the data on base.

Example :

.. code-block:: python

   from pyJoules.handler.mongo_handler import MongoHandler
   mongo_handler = MongoHandler(uri='mongodb://localhost', database_name='db', collection_name='collection')
		
   with EnergyContext(handler=mongo_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
       foo()
       ctx.record(tag='bar')
       bar()

   mongo_handler.save_data()

Output
------

The previous example will store the following record on mongo db database

.. code-block:: JSON

  {
     "name":"trace_0",
     "trace":[
        {
           "timestamp":"AAAA",
           "tag":"foo",
           "duration":"BBBB",
           "energy":{
              "package_0":"CCCC",
              "nvidia_gpu_0":"DDDD"
           }
        },
        {
           "timestamp":"AAAA2",
           "tag":"bar",
           "duration":"BBBB2",
           "energy":{
              "package_0":"CCCC2",
              "nvidia_gpu_0":"DDDD2"
           }
        }
     ]
  }

with :

- AAAA* : timestamp of the measured interval beginning
- BBBB* duration of the measured interval (in seconds)
- CCCC* energy consumed by CPU 0 during the measured interval
- DDDD* energy consumed by GPU 0 during the measured interval

Trace name
^^^^^^^^^^

Each trace stored in the database is named. Trace name is computed by adding an integer (which is incremented each time a new trace is stored) to a string prefix. By default, this prefix is ``trace`` so the first trace you store will be named ``trace_0``, the second ``trace_1``.

You can change this default prefix by specifying the ``trace_name_prefix`` with the prefix you want to use.
