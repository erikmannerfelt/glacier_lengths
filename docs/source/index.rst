.. xdem documentation master file, created by
   sphinx-quickstart on Fri Mar 19 14:30:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to glacier_lengths's documentation!
===========================================
Often when glacier lengths are calculated, only the glacier centerline is considered.
This is arguably not a statistically representative measure for the entire front, as it just considers one point on the glacier outline.
The `glacier_lengths` package aims to simplify length calculations along an arbitrary amount of lines buffered around the glacier centerline.

Simple usage
==================

.. literalinclude:: code/simple_usage.py
        :language: python

prints:

.. program-output:: python code/simple_usage.py


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/glacier_lengths.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
