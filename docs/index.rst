.. pyRAPL documentation master file, created by
   sphinx-quickstart on Tue Oct  8 14:16:48 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: raw-role(raw)
   :format: html latex

Welcome to pyRAPL's documentation!
**********************************

.. toctree::
   :maxdepth: 3

   quickstart
   API
   Outputs_API


About
=====

**pyRAPL** is a software toolkit to measure the energy footprint of a host machine along the execution of a piece of Python code.

**pyRAPL** uses the Intel "*Running Average Power Limit*" (RAPL) technology that estimates power consumption of a CPU. This technology is available on Intel CPU since the `Sandy Bridge`__ generation.

__ https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits

More specifically, pyRAPL can measure the energy consumption of the following CPU domains:

- CPU socket package
- DRAM (for server architectures)
- GPU (for client architectures)

Miscellaneous
=============

PyRAPL is an open-source project developed by the `Spirals research group`__ (University of Lille and Inria) that take part of the Powerapi_ initiative.

.. _Powerapi: http://powerapi.org

__ https://team.inria.fr/spirals

Mailing list and contact
^^^^^^^^^^^^^^^^^^^^^^^^

You can contact the developer team with this address : :raw-role:`<a href="mailto:powerapi-staff@inria.fr">powerapi-staff@inria.fr</a>`

You can follow the latest news and asks questions by subscribing to our :raw-role:`<a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>`

Contributing
^^^^^^^^^^^^

If you would like to contribute code you can do so via GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing coding conventions and style in order to keep the code as readable as possible.
