Print Handler
*************

This handler print the measured energy sample on the standard output

How to Use it
-------------

This handler is the default handler. When you use a context manager and decorated function without specifying any handler, the ``PrintHandler`` will be used

Example :

.. code-block:: python

   with EnergyContext(domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
       foo()
       ctx.record(tag='bar')
       bar()

Output
------
The previous example will produce the following result on the standard output


.. code-block::
   
   begin timestamp : AAAA; tag : foo; duration : BBBB; package_0 : CCCC; nvidia_gpu_0 : DDDD
   begin timestamp : AAAA2; tag : bar; duration : BBBB2; package_0 : CCCC2; nvidia_gpu_0 : DDDD2

with :

- AAAA* : timestamp of the measured interval beginning
- BBBB* duration of the measured interval (in seconds)
- CCCC* energy consumed by CPU 0 during the measured interval
- DDDD* energy consumed by GPU 0 during the measured interval
