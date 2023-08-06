====================
Simple Guided Optics
====================

A small collection of several classical methods for guided optics.



General description
___________________

The package written in Python during my PhD which I didn't achevie. The main benefit of the package is that it is written in an OOP logic. One can create and manipulate such classes as Waveguide and Simulation and deal with them in the abstraction of the calculation methods.

The package contains the following features:

* The calculatiion of propagation constant, effective index, group velocity, GDD, D2 frequency depencences;
* Frequency dependent material parameters are supported as well as constant ones;

* Planar geometry is resolved analytically (Pollock Lipson);
* Slab geometry is resolved with the famework of a modified Marcatili method (Menon, 2002);
* Goell's method is supported as well;



Putting the package on use
__________________________

There are two main classes in the package ``Waveguide`` and ``Simulation``. By calling the ``Waveguide`` instance, the waveguide can be created. Initially, it contains the following attributes:

* height, width in micrometers;

* substrate, core and cladding materials;

- in the case of a rectandular cross-section there will be only the cladding;

The ``Simulation`` class contains the parameters which define the simulation itself. They are as follows:

* calculation units: wavelength, frequency and V-number;

* start, stop, step, points, span (any three of choice).

After the simulation has been initialised, and before it has been run, the waveguide obtains the following properties:

* core, substrate, cladding permettivities and refractive indices.

After the simulation is completed, the waveguide obtains another set of arguments:

* propagation constant (``beta``);

* effective index (``neff``);

* group index (``ng``);

* group delay dispersion (``GDD``);

There parameters can be called as properties, or as methods pricising the calculation point::

ng(wavelength=1.55)





Features to come asap
_____________________

* Coupled wave solutions for waveguide Bragg gratings: planar, slab, TE/TM modes propagation/radiation type;
* Several primitive devices such as rings (add-drop, all pass), modulators;
* Pulse propagation in linear media;





Installation 
____________
Installes via PyPI as 