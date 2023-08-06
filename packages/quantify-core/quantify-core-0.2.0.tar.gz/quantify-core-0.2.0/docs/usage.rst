===============
User guide
===============

Introduction
===============

A :mod:`Quantify` experiment typically consists of a data-acquisition loop in which one or more parameters are set and one or more parameters are measured.

Core concepts
====================

The core of Quantify can be understood by understanding the following concepts:

- `Parameter`_
- `Instrument`_
- `Measurement Control`_
- `Data storage & Analysis`_

Parameter
-----------

A parameter represents a state variable of the system.

    - A parameter can be get and/or set able.
    - Contains metadata such as units and labels.
    - Commonly implemented using the QCoDeS :class:`~qcodes.instrument.parameter.Parameter` class.


Instrument
-----------

An Instrument is a container for parameters that typically (but not necesarily) corresponds to a physical piece of hardware.

Instruments provide the following functionality.

- Container for parameters.
- A standardized interface.
- Provide logging of parameters through the :meth:`~qcodes.instrument.base.Instrument.snapshot` method.
- All instruments inherit from the QCoDeS :class:`~qcodes.instrument.base.Instrument` class.


Measurement Control
-------------------

The :class:`~quantify.measurement.MeasurementControl` (MC) is in charge of the data-acquisition loop and is based on the notion that, in general, an experiment consists of the following three steps:

1. Initialize (set) some parameter(s),
2. Measure (get) some parameter(s),
3. Store the data.

Quantify provides two helper classes, Settable and Gettable to aid in these steps, which are explored further in later sections of this article.

:class:`~quantify.measurement.MeasurementControl` provides the following functionality

- Enforce standardization of experiments
- Standardized data storage
- Live plotting of the experiment
- n-dimensional sweeps
- Data acquisition controlled by software or hardware
- Adaptive sweeps (measurement points are not predetermined at the beginning of an experiment)


Basic example, a 1D software-controlled measurement loop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running an experiment is simple!
Simply define what parameters to set, and get, and what points to loop over.

In the example below we want to set frequencies on a microwave source and acquire the signal from the pulsar readout module.

.. code-block:: python

    MC.settables(mw_source1.freq)               # We want to set the frequency of a microwave source
    MC.setpoints(np.arange(5e9, 5.2e9, 100e3))  # Scan around 5.1 GHz
    MC.gettables(pulsar_QRM.signal)             # acquire the signal from the pulsar AQM
    dataset = MC.run(name='Frequency sweep')    # Start the experiment


The MeasurementControl can also be used to perform more advanced experiments such as 2D scans, pulse-sequences where the hardware is in control of the acquisition loop, or adaptive experiments in which it is not known what data points to acquire in advance, they are determined dynamically during the experiment.
Take a look at "nonexistent_example_notebook" for a tutorial on the MeasurementControl.


Control Mode
------------

A very important aspect in the usage of the MeasurementControl is the Control Mode, which specifies whether the MC itself dictates how the setpoints are iterated through, or whether an external device does.
These modes are referred to as *Software* in the former case and *Hardware* in the latter.

The benefit provided by this differentiation is in overhead reduction; it is often costly to transmit (large) blocks of data to external devices.
In *Software* mode, the MC steps through each setpoint one at a time, processing them one by one.
In *Hardware* mode, the MC vectorises the setpoints such that they are processed in a batch.
Control mode is detected automatically based on the attributes of the Gettables; this is expanded upon in subsequent sections.


Settable and Gettable
----------------------

The interfaces for Settable and Gettable parameters are encapsulated in the :class:`~quantify.measurement.Settable` and :class:`~quantify.measurement.Gettable` helper classes respectively.
We set values to Settables; these values populate an x-axis. Similarly, we get values from Gettables which populate a y-axis.
These classes define a set of mandatory and optional attributes the MeasurementControl recognizes and will use as part of the experiment, which are expanded up in the API Reference.

Depending on which Control Mode the MeasurementControl is running in, the interfaces for Settables and Gettables are slightly different:

**Software Controlled:**

- Each settable accepts a single float value.
- Gettables return a single float value, **OR**
- Gettables return a 1D array of floats, with each element corresponding to a *different y dimension*.

**Hardware Controlled:**

- Each settable accepts a 1D array of float values corresponding to all setpoints for a single *X dimension*.
- Gettables return a 1D array of float values with each element corresponding to the datapoints *in that Y dimension*, **OR**
- Gettables return a 2D array of float values with each row representing a *different Y dimension* with the above structure, i.e. each column is a datapoint corresponding to each setpoint.

.. note::
    It is also possible for a Hard Gettables to return a partial array with length less than the input. This is helpful when working with resource constrained devices,
    for example if you have *n* setpoints but your device can load only less than *n* datapoints into memory. In this scenario, the MC tracks how many datapoints were actually
    processed, automatically adjusting the size of the next batch.

For ease of use, we do not require users to inherit from a Gettable/Settable class, and instead provide contracts in the form of JSON schemas to which these classes must fit.
In addition to using a library which fits these contracts (such as the QCodes.Parameter family of classes) we can define our own Settables and Gettables.
Below we create a Soft Gettable which returns values in two dimensions, one Sine wave and a Cosine wave, using a QCodes Settable:

.. jupyter-execute::

    import numpy as np
    from qcodes import ManualParameter


    t = ManualParameter('time', label='Time', unit='s')

    class DualWave:
        def __init__(self):
            self.unit = ['V', 'V']
            self.label = ['Amplitude', 'Amplitude']
            self.name = ['sine', 'cosine']

        def get(self):
            return np.array([np.sin(t() / np.pi), np.cos(t() / np.pi)])


.soft, .prepare() and .finish()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MeasurementControl checks for 3 other optional properties on settables/gettables, the ``soft`` attribute and the ``prepare()`` and ``finish()`` methods.
``soft`` declares which Control Mode this parameter runs in. It defaults to ``True`` (i.e., software controlled). All Gettables must currently have the same setting;
this defines which Control Mode the experiment will run in.

The ``prepare()`` and ``finish()`` methods are useful for performing work before each iteration of the measurement loop and once after completion.
For example, arming a piece of hardware with data and then closing a connection upon completion.

Data storage & Analysis
=========================
As well as the produced dataset, every :class:`qcodes.instrument.parameter.Parameter` and QCodes Instrument in an
experiment run by Quantify is automatically serialized to disk.

This is intended to aid with reproducibility, as a past experiment can be easily reloaded and re-run by anyone.

Concepts
----------

Data Directory
~~~~~~~~~~~~~~~~

The top level directory in the file system where output is saved to. Experiments are first grouped by date -
all experiments which take place on a certain date will be saved together in a subdirectory in the form ``YYYYmmDD``.

Experiment Container
~~~~~~~~~~~~~~~~~~~~

Individual experiments are saved to their own subdirectories (of the Data Directory) named based on the :class:`~quantify.data.types.TUID` and the ``<experiment name (if any)>``.

.. note::
    TUID: A Time-based Unique ID is of the form ``YYYYmmDD-HHMMSS-sss-<random 6 character string>`` and these subdirectories' names take the form ``YYYYmmDD-HHMMSS-sss-<random 6 character string><-experiment name (if any)>``.

These subdirectories are termed 'Experiment Containers', typical output being the Dataset in hdf5 format and a JSON format file describing Parameters, Instruments and such.

Furthermore, additional analysis such as fits can also be written to this directory, storing all data in one location.

A data directory with the name 'MyData' thus will look similar to:

- MyData
    - 20200708
        - 20200708-145048-800-60cf37
        - 20200708-145205-042-6d068a-bell_test
            - dataset.hdf5
            - snapshot.json
            - lmfit.png
    - 20200710

.. note::
    The root directory of all experiments being used by Quantify can be retrieved/set with :meth:`~quantify.data.handling.get_datadir`/:meth:`~quantify.data.handling.set_datadir`.

Dataset
~~~~~~~~~

The output produced by the experiment, stored in HDF5 format. This topic is expanded upon in the :ref:`DataStorage specification`.

Snapshot
~~~~~~~~~~

The configuration for each QCodes Instrument used in this experiment. This information is automatically collected for all Instruments in use.
It is useful for quickly reconstructing a complex set-up or verifying that :class:`qcodes.instrument.parameter.Parameter` objects are as expected.
