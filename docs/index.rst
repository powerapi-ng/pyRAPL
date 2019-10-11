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

pyRAPL is a toolkit that measures the power consumption of a machine during the
execution of a python piece of code.

pyRAPL use the intel "Running Average Power Limit" (RAPL) technology that
estimate global power consumption of internal devices. This technology is only available
on Intel CPU with Sandy Bridge architecture or higher.

pyRAPL can measure the power consumption of the following devices:

- CPU socket package 
- RAM (only on server CPU)

Miscellaneous
=============

PyRAPL is an open-source project developed by the `Spirals research group`__ (University of Lille and Inria) that take part of the [powerapi](powerapi.org) project.

__ https://team.inria.fr/spirals

The documentation is available here_.

.. _here: https://pyrapl.readthedocs.io/en/latest/

Mailing list and contact
^^^^^^^^^^^^^^^^^^^^^^^^

You can contact the developer team with this address : :raw-role:`<a href="mailto:powerapi-staff@inria.fr">powerapi-staff@inria.fr</a>`

You can follow the latest news and asks questions by subscribing to our :raw-role:`<a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>`

Contributing
^^^^^^^^^^^^

If you would like to contribute code you can do so through GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible.
