.. pyJoules documentation master file, created by
   sphinx-quickstart on Tue Oct  8 14:16:48 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: raw-role(raw)
   :format: html latex

Welcome to pyJoules's documentation!
************************************
	    
About
=====

**pyJoules** is a software toolkit to measure the energy footprint of a host machine along the execution of a piece of Python code.
It monitors the energy consumed by specific device of the host machine such as :

- intel CPU socket package
- RAM (for intel server architectures)
- intel integrated GPU (for client architectures)
- nvidia GPU

Limitation
----------

CPU, RAM and integrated GPU
^^^^^^^^^^^^^^^^^^^^^^^^^^^
**pyJoules** uses the Intel "*Running Average Power Limit*" (RAPL) technology that estimates energy consumption of the CPU, ram and integrated GPU.
This technology is available on Intel CPU since the `Sandy Bridge generation`__ (2010).

__ https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits

For the moment, **pyJoules** use the linux kernel API to get energy values reported by RAPL technology. That's why CPU, RAM and integrated GPU energy monitoring is not available on windows or MacOS.

As RAPL is not provided by a virtual machine, **pyJoules** can't use it anymore to monitor energy consumption inside a virtual machine.

Nvidia GPU
^^^^^^^^^^
**pyJoules** uses the nvidia "*Nvidia Management Library*" technology to measure energy consumption of nvidia devices. The energy measurement API is only available on nvidia GPU with `Volta architecture`__ (2018)

__ https://en.wikipedia.org/wiki/Volta_(microarchitecture)

Monitor only function energy consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**pyjoules** monitor device energy consumption. The reported energy consumption is not only the energy consumption of the code you are running. This includes the *global energy consumption* of all the process running on the machine during this period, thus including the operating system and other applications.

That is why we recommend to eliminate any extra programs that may alter the energy consumption of the machine hosting experiments and to keep only the code under measurement (*i.e.*, no extra applications, such as graphical interface, background running task...). This will give the closest measure to the real energy consumption of the measured code.

Quickstart
==========

Installation
------------

You can install **pyJoules** with pip : ``pip install pyJoules``

Decorate a function to measure its energy consumption
-----------------------------------------------------

To measure the energy consumed by the machine during the execution of the
function ``foo()`` run the following code::

To measure the energy consumed by the machine during the execution of the function ``foo()`` run the following code with the :raw-role:`<a href="API/main_api.html#pyJoules.energy_meter.measure_energy">` ``measure_energy`` :raw-role:`</a>` decorator:

.. code-block:: python

   from pyJoules.energy_meter import measure_energy

   @measure_energy
   def foo():
       # Instructions to be evaluated.

   foo()


This will print in the console the recorded energy consumption of all the monitorable devices during the execution of function ``foo``.

  

Miscellaneous
=============

PyJoules is an open-source project developed by the `Spirals research group`__ (University of Lille and Inria) that take part of the Powerapi_ initiative.

.. _Powerapi: http://powerapi.org

__ https://team.inria.fr/spirals

Mailing list and contact
------------------------

You can contact the developer team with this address : :raw-role:`<a href="mailto:powerapi-staff@inria.fr">powerapi-staff@inria.fr</a>`

You can follow the latest news and asks questions by subscribing to our :raw-role:`<a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>`

Contributing
------------

If you would like to contribute code you can do so via GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing coding conventions and style in order to keep the code as readable as possible.


Table of contents
=================

.. toctree::
   :maxdepth: 2

   About <self>
   usages/usage
   handlers/handlers
   devices/devices
   API/API.rst
