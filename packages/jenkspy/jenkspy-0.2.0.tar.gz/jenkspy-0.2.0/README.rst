Fast Jenks breaks for Python
============================

Compute "natural breaks" (*Fisher-Jenks algorithm*) on list / tuple / array / numpy.ndarray of integers/floats.

Intented compatibility: CPython 3.4+

Wheels are provided via PyPI for windows users - Also available on conda-forge channel for Anaconda users

|Version| |Anaconda-Server Badge| |Build Status travis| |Build status appveyor| |PyPI download month|

Usage :
-------

This package consists of a single function (named `jenks_breaks`) which takes as input a `list <https://docs.python.org/3/library/stdtypes.html#list>`_ / `tuple <https://docs.python.org/3/library/stdtypes.html#tuple>`_ / `array.array <https://docs.python.org/3/library/array.html#array.array>`_ / `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ of integers or floats.
It returns a list of values that correspond to the limits of the classes (starting with the minimum value of the series - the lower bound of the first class - and ending with its maximum value - the upper bound of the last class).




.. code:: python

    >>> import jenkspy
    >>> import random
    >>> list_of_values = [random.random()*5000 for _ in range(12000)]

    >>> breaks = jenkspy.jenks_breaks(list_of_values, nb_class=6)

    >>> breaks
	(0.1259707312994962, 1270.571003315598, 2527.460251085392, 3763.0374498649376, 4999.87456576267)

    >>> import json
    >>> with open('tests/test.json', 'r') as f:
    ...     data = json.loads(f.read())
    ...
    >>> jenkspy.jenks_breaks(data, nb_class=5) # Asking for 5 classes
    (0.0028109620325267315, 2.0935479691252112, 4.205495140049607, 6.178148351609707, 8.09175917180255, 9.997982932254672)
    # ^                      ^                    ^                 ^                  ^                 ^
    # Lower bound            Upper bound          Upper bound       Upper bound        Upper bound       Upper bound
    # 1st class              1st class            2nd class         3rd class          4th class         5th class
    # (Minimum value)                                                                                    (Maximum value)



This package also support a `JenksNaturalBreaks` (require `NumPy`) class as interface (inspired by `scikit-learn` classes). The `.fit` and `.group` behavior is slightly different from `jenks_breaks`, by accepting value outside the range of the minimum and maximum value of `breaks_`, retaining the input size. It means that fit and group will use only the `inner_bound_`. All value below the min bound will be included in the first group and all value higher than the max bound will be included in the last group.



.. code:: python

    >>> from jenkspy import JenksNaturalBreaks

    >>> x = [0,1,2,3,4,5,6,7,8,9,10,11]

    >>> jnb = JenksNaturalBreaks()

    >>> try:
    ...     print(jnb.labels_)
    ...     print(jnb.groups_)
    ...     print(jnb.inner_breaks_)
    >>> except:
    ...     pass

    >>> jnb.fit(x)
    >>> try:
    ...     print(jnb.labels_)
    ...     print(jnb.groups_)
    ...     print(jnb.inner_breaks_)
    >>> except:
    ...     pass
    [0 0 0 1 1 1 2 2 2 3 3 3]
    [array([0, 1, 2]), array([3, 4, 5]), array([6, 7, 8]), array([ 9, 10, 11])]
    [2.0, 5.0, 8.0]

    >>> print(jnb.predict(15))
    3

    >>> print(jnb.predict([2.5, 3.5, 6.5]))
    [1 1 2]

    >>> print(jnb.group([2.5, 3.5, 6.5]))
    [array([], dtype=float64), array([2.5, 3.5]), array([6.5]), array([], dtype=float64)]


Installation
------------

+ **From pypi**

.. code:: shell

    pip install jenkspy


+ **From source**

.. code:: shell

    git clone http://github.com/mthh/jenkspy
    cd jenkspy/
    python setup.py install


+ **For anaconda users**

.. code:: shell

    conda install -c conda-forge jenkspy


Requirements :
----------------------------------------------

-  NumPy\ :sup:`*` 
-  C compiler\ :sup:`+`
-  Python C headers\ :sup:`+`

\ :sup:`*` only for using `JenksNaturalBreaks` interface

\ :sup:`+` only for building from source

Motivation :
------------

-  Making a painless installing C extension so it could be used more easily
   as a dependency in an other package (and so learning how to build wheels
   using *appveyor*).
-  Getting the break values! (and fast!). No fancy functionnality provided,
   but contributions/forks/etc are welcome.
-  Other python implementations are currently existing but not as fast nor available on PyPi.

.. |Build Status travis| image:: https://travis-ci.org/mthh/jenkspy.svg?branch=master
   :target: https://travis-ci.org/mthh/jenkspy

.. |Build status appveyor| image:: https://ci.appveyor.com/api/projects/status/9ffk6juf2499xqk0/branch/master?svg=true
   :target: https://ci.appveyor.com/project/mthh/jenkspy/branch/master

.. |Version| image:: https://img.shields.io/pypi/v/jenkspy.svg
   :target: https://pypi.python.org/pypi/jenkspy

.. |Anaconda-Server Badge| image:: https://anaconda.org/conda-forge/jenkspy/badges/version.svg
   :target: https://anaconda.org/conda-forge/jenkspy

.. |PyPI download month| image:: https://img.shields.io/pypi/dm/jenkspy.svg
   :target: https://pypi.python.org/pypi/jenkspy
