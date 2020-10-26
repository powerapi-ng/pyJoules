Context manager
***************

Use a context manager to add tagged "breakpoint" in your measurement
--------------------------------------------------------------------
If you want to know where is the *hot spots* where your python code consume the
most energy you can add *breakpoints* during the measurement process and tag
them to know amount of energy consumed between this breakpoints.

For this, you have to use a context manager to measure the energy
consumption. It is configurable as the :raw-role:`<a href="decorator.html">` decorator :raw-role:`</a>`. For example, here we use an
:raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyContext">` ``EnergyContext`` :raw-role:`</a>` to measure the energy consumption of CPU ``1`` and nvidia gpu ``0``
and report it in a csv file

.. code-block:: python

   from pyJoules.energy_meter import EnergyContext
   from pyJoules.device.rapl_device import RaplPackageDomain
   from pyJoules.device.nvidia_device import NvidiaGPUDomain
   from pyJoules.handler.csv_handler import CSVHandler
	
   csv_handler = CSVHandler('result.csv')
	
   with EnergyContext(handler=csv_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
       foo()
       ctx.record(tag='bar')
       bar()

   csv_handler.save_data()

This will record the energy consumed :

- between the beginning of the :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyContext">` ``EnergyContext`` :raw-role:`</a>` and the call of the ``ctx.record`` method
- between the call of the ``ctx.record`` method and the end of the :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyContext">` ``EnergyContext`` :raw-role:`</a>`

Each measured part will be written in the csv file. One line per part.
