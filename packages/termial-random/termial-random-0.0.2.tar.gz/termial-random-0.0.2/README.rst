Implementation of termial random
--------------------------------

This minimalistic CPython extension provides termial random implementation.


See `this
<https://medium.com/@fridex/termial-random-for-prioritized-picking-an-item-from-a-list-a65a4f563224>`__
and `this
<https://medium.com/@fridex/optimizing-termial-random-by-removing-binomial-coefficient-e39b9ca7aaa3>`__
article for more info on termial random.

Basically, the random generator prioritizes numbers closer to 0. See the
distribution plotted below for n==10.

.. image:: https://github.com/fridex/termial-random/raw/main/fig/distribution.png
   :target: https://github.com/fridex/termial-random/raw/main/fig/distribution.png
   :alt: Distribution of numbers generated using termial random.

Installation
============

Simply install this library using pip:

.. code-block:: console

  pip install termial-random

Usage
=====

The module provides 3 core routines:

* ``termial_random.seed(n)`` used to initialie glibc random number generator based on ``n`` provided
* ``termial_random.seed_init()`` used to initialie glibc random number generator based on the current time
* ``termial_random.random(n)`` used to compute termial random number for the given ``n``

Benchmarks
==========

See `this gist with benchmarks <https://gist.github.com/fridex/3794b9cbb35d1b8f523a94ee9d86b8e4>`__.
