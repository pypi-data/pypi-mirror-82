=============
Pyxel-Physics
=============

Physics engine that merges Pyxel with Pymunk.

Installation
============

Clone repository and use ``flit install -s`` to install locally or 
``pip install pyxel-physics``, if you do not want to participate in the 
development of Pyxel Physics.


Tutorial
========

The folllowing code simulates a gas of spheres. Let us start importing some modules. 

.. code-block:: python

    from random import uniform

    import pyxel
    import phys


First, we initialize pyxel and set the gravity in the space object.

.. code-block:: python

    pyxel.init(120, 80, fps=60)
    space = phys.space(gravity=(0, 25))


Secondly, let us create some object in the screen. ``phys.circ`` produces
a Circle body using an API similar to pyxel. Pyxel physics also has 
functions such as ``rect``, ``tri``, ``line`` and ``poly`` that behaves 
similarly. 

.. code-block:: python

    radius = 2
    for _ in range(50):
        x, y = uniform(0, 120), uniform(0, 80)
        phys.circ(x, y, radius, vel=(uniform(-25, 25), uniform(-25, 25)))

   phys.margin(col=pyxel.COLOR_RED)


We can start the main loop using the default pyxel mechanisms, or simply
executing the run() method of space objects. 

.. code-block:: python

    space.run()
