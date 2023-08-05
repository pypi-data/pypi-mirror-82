Randen: Random DataFrame Generator
==================================
.. image:: https://raw.githubusercontent.com/varskann/randen/main/docs/source/_static/randen.PNG


**Randen** is a minimal utility module for generating Pandas dataframes
It exposes a handful of methods to quickly generate big random dataframes.


How to Install
--------------

Randen can be installed as like any other python module, via pip

::

    pip install randen


Basic Usage
-----------
Within the python script::

    from randen import DataFrameGenerator
    dfg = DataFrameGenerator()
    data_frame = dfg.get_dataframe(...)


Motivation
----------
Recently, while benchmarking Pandas binary file format I/O for a project, I needed to
generate multiple big dataframes. Hence, publishing this utility as a package to reduce redundant ad-hoc work

If you need some enhancements in the package, feel free to raise a Pull request or drop
a note to varskann993@gmail.com

If this isn't what you need at all,
enjoy a trip to the original `Randen <https://en.wikipedia.org/wiki/Randen_(mountain_range)>`_.
