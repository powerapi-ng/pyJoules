.. pyRAPL documentation master file, created by
   sphinx-quickstart on Tue Oct  8 14:16:48 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: raw-role(raw)
   :format: html latex

Welcome to pyJoules's documentation!
************************************

.. toctree::
   :maxdepth: 3

   quickstart
   API
   Device_API
   Handler_API

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
**pyJoules** uses the Intel "*Running Average Power Limit*" (RAPL) technology that estimates power consumption of the CPU, ram and integrated GPU.
This technology is available on Intel CPU since the `Sandy Bridge generation`__ (2010).

__ https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits

Nvidia GPU
^^^^^^^^^^
**pyJoules** uses the nvidia "*Nvidia Management Library*" technology to measure energy consumption of nvidia devices. The energy measurement API is only available on nvidia GPU with `Volta architecture`__ (2018)

__ https://en.wikipedia.org/wiki/Volta_(microarchitecture)
  

Miscellaneous
=============

PyRAPL is an open-source project developed by the `Spirals research group`__ (University of Lille and Inria) that take part of the Powerapi_ initiative.

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
