Pandas Handler
**************

This Handler save the measured energy sample on a panda Dataframe

How to Use it
-------------

Create a ``PandasHandler`` instance and pass it as a parameter of the context manager or the function decorator.

When the measure is done, you can retrieve the dataframe using the ``get_dataframe`` method

Example :

.. code-block:: python

   from pyJoules.handler.pandas_handler import PandasHandler
   pandas_handler = PandasHandler()
		
   with EnergyContext(handler=pandas_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
       foo()
       ctx.record(tag='bar')
       bar()

   df = pandas_handler.get_dataframe()

Output
------

This will produce the following dataframe :

.. code-block::

     timestamp  tag  duration  package_0  nvidia_gpu_0
   0  AAAA  foo     BBBB        CCCC        DDDD
   1  AAAA2  bar     BBBB2        CCCC2        DDDD2

with :

- AAAA* : timestamp of the measured interval beginning
- BBBB* duration of the measured interval (in seconds)
- CCCC* energy consumed by CPU 0 during the measured interval
- DDDD* energy consumed by GPU 0 during the measured interval

