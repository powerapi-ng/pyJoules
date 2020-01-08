Quickstart
**********

Installation
============

You can install **pyRAPL** with pip : ``pip install pyRAPL``

Basic usage
===========

Here are some basic usages of **pyRAPL**. Please note that the reported energy consumption is not only the energy consumption of the code you are running. This includes the *global energy consumption* of all the process running on the machine during this period, thus including the operating system and other applications.

That is why we recommend to eliminate any extra programs that may alter the energy consumption of the machine hosting experiments and to keep only the code under measurement (*i.e.*, no extra applications, such as graphical interface, background running task...). This will give the closest measure to the real energy consumption of the measured code.

Decorate a function to measure its energy consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure the energy consumed by the machine during the execution of the
function ``foo()`` run the following code::

To measure the energy consumed by the machine during the execution of the function ``foo()`` run the following code with the :raw-role:`<a href="API.html#pyJoules.energy_meter.measureit">` ``measureit`` :raw-role:`</a>` decorator:

.. code-block:: python

   from pyJoules.energy_meter import measureit

   @measureit
   def foo():
       # Instructions to be evaluated.

   foo()


This will print in the console the recorded energy consumption of all the monitorable devices during the execution of function ``foo``.

Configure the decorator specifying the device to monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can easily configure which device to monitor using the parameters of the :raw-role:`<a href="API.html#pyJoules.energy_meter.measureit">` ``measureit`` :raw-role:`</a>` decorator. 
For example, the following example only monitors the CPU power consumption on the CPU socket ``1`` and the Nvidia GPU ``0``.
By default, **pyJoules** monitors all the available devices of the CPU sockets.

__ free.fr

.. code-block:: python

   from pyJoules.energy_meter import measureit
   from pyJoules.energy_device.rapl_device import RaplPackageDomain
   from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain
	
   @measureit(domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)])
   def foo():
       # Instructions to be evaluated.

   foo()	

You can append the following domain list to monitor them : 
	
- :raw-role:`<a href="Device_API.html#pyJoules.energy_device.rapl_device.RaplPackageDomain">` ``pyJoules.energy_device.rapl_device.RaplPackageDomain`` :raw-role:`</a>`: CPU (specify the socket id in parameter)
- :raw-role:`<a href="Device_API.html#pyJoules.energy_device.rapl_device.RaplDramDomain">` ``pyJoules.energy_device.rapl_device.RaplDramDomain`` :raw-role:`</a>`: RAM (specify the socket id in parameter)
- :raw-role:`<a href="Device_API.html#pyJoules.energy_device.rapl_device.RaplUncoreDomain">` ``pyJoules.energy_device.rapl_device.RaplUncoreDomain`` :raw-role:`</a>`: integrated GPU (specify the socket id in parameter)
- :raw-role:`<a href="Device_API.html#pyJoules.energy_device.rapl_device.RaplCoreDomain">` ``pyJoules.energy_device.rapl_device.RaplCoreDomain`` :raw-role:`</a>`: RAPL Core domain (specify the socket id in parameter)
  
..
   - :raw-role:`<a href="Device_API.html#pyJoules.energy_device.nvidia_device.NvidiaGPUDomain">` ``pyJoules.energy_device.nvidia_device.NvidiaGPUDomain`` :raw-role:`</a>`: Nvidia GPU (specify the socket id in parameter)
   

Configure the output of the decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to handle data with different output than the standard one, you can configure the decorator with an :raw-role:`<a href="Handler_API.html#pyJoules.energy_handler.EnergyHandler">` ``EnergyHandler`` :raw-role:`</a>` instance from the ``pyJoules.energy_handler`` module.

As an example, if you want to write the recorded energy consumption in a .csv file:

.. code-block:: python

   from pyJoules.energy_meter import measureit
   from pyJoules.energy_handler import CsvHandler
	
   csv_handler = CsvHandler('result.csv')
	
   @measureit(handler=csv_handler)
   def foo():
   # Instructions to be evaluated.

   for _ in range(100):
       foo()
		
   csv_output.save()
   
This will produce a csv file of 100 lines. Each line containing the energy
consumption recorded during one execution of the function ``foo``.
Other predefined ``Handler`` classes exist to export data to *MongoDB* and *Panda*
dataframe.
You can also create your own Output class (see the documentation_)

.. _documentation: https://pyrapl.readthedocs.io/en/latest/Outputs_API.html

Use a context manager to add tagged "_breakpoint_" in your measurment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to know where is the *hot spots* where your python code consume the
most energy you can add *breakpoints* during the measurement process and tag
them to know amount of energy consumed between this breakpoints.

For this, you have to use a context manager to measure the energy
consumption. It is configurable as the decorator. For example, here we use an
:raw-role:`<a href="API.html#pyJoules.energy_meter.EnergyContext">` ``EnergyContext`` :raw-role:`</a>` to measure the power consumption of CPU ``1`` and nvidia gpu ``0``
and report it in a csv file

.. code-block:: python

   from pyJoules.energy_meter import EnergyContext
   from pyJoules.energy_device.rapl_device import RaplPackageDomain
   from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain
   from pyJoules.energy_handler import CsvHandler
	
   csv_handler = CsvHandler('result.csv')
	
   with EnergyContext(handler=csv_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx
       foo()
       ctx.record(tag='bar')
       bar()

   csv_handler.save()

This will record the energy consumed ::

- between the beginning of the :raw-role:`<a href="API.html#pyJoules.energy_meter.EnergyContext">` ``EnergyContext`` :raw-role:`</a>` and the call of the ``ctx.record`` method
- between the call of the ``ctx.record`` method and the end of the :raw-role:`<a href="API.html#pyJoules.energy_meter.EnergyContext">` ``EnergyContext`` :raw-role:`</a>`

Each measured part will be written in the csv file. One line per part.
