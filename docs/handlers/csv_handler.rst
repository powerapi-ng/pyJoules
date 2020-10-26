CSV Handler
***********

This handler save the measured energy sample on a csv file

How to Use it
-------------

Create a ``CSVHandler`` instance and pass it as a parameter of the context manager or the function decorator. You have to specify the filename of the file that will store the energy sample.

When the measure is done, you have to use the ``save_data`` method to write the data on disk.

Example :

.. code-block:: python

   from pyJoules.handler.csv_handler import CSVHandler
   csv_handler = CSVHandler('result.csv')
		
   with EnergyContext(handler=csv_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
       foo()
       ctx.record(tag='bar')
       bar()

   csv_handler.save_data()

Output
------

The previous example will produce the following csv file ``result.csv``

.. code-block::

   timestamp;tag;duration;package_0;nvidia_gpu_0
   AAAA;foo;BBBB;CCCC;DDDD
   AAAA2;bar;BBBB2;CCCC2;DDDD2

with :

- AAAA* : timestamp of the measured interval beginning
- BBBB* duration of the measured interval (in seconds)
- CCCC* energy consumed by CPU 0 during the measured interval
- DDDD* energy consumed by GPU 0 during the measured interval
