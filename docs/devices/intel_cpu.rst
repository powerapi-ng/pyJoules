Intel CPU
*********

PyJoules support energy consumption monitoring of intel cpu using the "Running Average Power Limit" (RAPL) technology. RAPL is available on CPU since the  `Sandy Bridge generation`__ (2010)

__ https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits

Domains
=======
You can monitor energy consumption from several part of a CPU, called domain.

Each monitorable domain is described on this image :

.. image:: https://raw.githubusercontent.com/powerapi-ng/pyJoules/master/rapl_domains.png

With :

- Package : correspond to the wall cpu energy consumption
- core : correpond to the sum of all cpu core energy consumption
- uncore : correspond to the integrated GPU

Usage
=====
To configure your function decorator, context manager or energy meter to measure specific part of a CPU, pass as ``domain`` attribute a list of instance of a subClass of ``pyJoules.device.rapl_device.RaplDomain`` corresponding to the domain you want to monitor.

For example, if you want to configure a context manager to measure the energy consumed by the Core domain follow this example :

.. code-block:: python

   from pyJoules.device.rapl_device import RaplCoreDomain
   with EnergyContext(domains=[RaplCoreDomain(0)):
       foo()

You can use the following class to select the list of domain you want to monitor : 
	
- ``RaplPackageDomain`` : whole CPU socket (specify the socket id in parameter)
- ``RaplDramDomain`` : RAM (specify the socket id in parameter)
- ``RaplUncoreDomain`` : integrated GPU (specify the socket id in parameter)
- ``RaplCoreDomain`` : RAPL Core domain (specify the socket id in parameter)
