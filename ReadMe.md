__Delta Symbol SymPy Expressions__

author: Jonathan Gutow <gutow@uwosh.edu>

date: August 2020

license: GPL V3+

This python module is intended to be used interactive Jupyter notebooks and adds a way to define symbols
for use in SymPy expressions that display as &Delta;`X` when SymPy
typesets the expressions. This is the abbreviation commonly used in physical science for `final(X) - initial(X)`.

_Setup/Installation_: Currently this tool is not available as a pip installable package. The file `DeltaSymbol.py`
must be available for import in the directory space of the active Jupyter notebook. To activate issue
the command: `from DeltaSymbol import *`. This does not import SymPy, which must be done separately.

Usage examples can be found in the docstrings and the demonstration Jupyter notebook `Demonstration DeltaSymbol Class.ipynb`. 

Try in binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gutow/DeltaSymbol.git/master)