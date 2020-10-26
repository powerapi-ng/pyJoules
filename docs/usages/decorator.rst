Decorator
*********

Decorate a function to measure its energy consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure the energy consumed by the machine during the execution of the
function ``foo()`` run the following code::

To measure the energy consumed by the machine during the execution of the function ``foo()`` run the following code with the :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.measure_energy">` ``measure_energy`` :raw-role:`</a>` decorator:

.. code-block:: python

   from pyJoules.energy_meter import measure_energy

   @measure_energy
   def foo():
       # Instructions to be evaluated.

   foo()


This will print in the console the recorded energy consumption of all the monitorable devices during the execution of function ``foo``.

Configure the decorator specifying the device to monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can easily configure which device to monitor using the parameters of the :raw-role:`<a href="/API/main_api.html#pyJoules.energy_meter.measure_energy">` ``measure_energy`` :raw-role:`</a>` decorator. 
For example, the following example only monitors the CPU energy consumption on the CPU socket ``1`` and the Nvidia GPU ``0``.
By default, **pyJoules** monitors all the available devices of the CPU sockets.

__ free.fr

.. code-block:: python

   from pyJoules.energy_meter import measure_energy
   from pyJoules.device.rapl_device import RaplPackageDomain
   from pyJoules.device.nvidia_device import NvidiaGPUDomain
	
   @measure_energy(domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)])
   def foo():
       # Instructions to be evaluated.

   foo()	

for more information about device you can monitor, see :raw-role:`<a href="../devices/devices.html">` here :raw-role:`</a>`:
   

Configure the output of the decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to handle data with different output than the standard one, you can configure the decorator with an :raw-role:`<a href="../API/Handler_API.html#pyJoules.handler.EnergyHandler">` ``EnergyHandler`` :raw-role:`</a>` instance from the :raw-role:`<a href="../API/Handler_API.html">` ``pyJoules.handler`` :raw-role:`</a>` module.

As an example, if you want to write the recorded energy consumption in a .csv file:

.. code-block:: python

   from pyJoules.energy_meter import measure_energy
   from pyJoules.handler.csv_handler import CSVHandler
	
   csv_handler = CSVHandler('result.csv')
	
   @measure_energy(handler=csv_handler)
   def foo():
   # Instructions to be evaluated.

   for _ in range(100):
       foo()
		
   csv_handler.save_data()
   
This will produce a csv file of 100 lines. Each line containing the energy
consumption recorded during one execution of the function ``foo``.
Other predefined ``Handler`` classes exist to export data to *MongoDB* and *Panda*
dataframe.
