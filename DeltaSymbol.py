# Extend the symbol class to generate a special symbol which is Delta of `X`
# where `X` is some symbol. Can be expanded into `Xf - Xi` (final - initial)
# to complete later calculations. Mostly for pretty math common to physical
# sciences (esp. thermodynamics).
# Jonathan Gutow <gutow@uwosh.edu>
# June 2020
# License: GPL V3+

from sympy import Symbol
import inspect


class DeltaSymbol(Symbol):
    """
    This class extends SymPy symbols to include Delta of a symbol ``X`` which
    is displayed as $\Delta{X}$ in Jupyter notebooks and the user chosen in
    python compatible character sequence in plain text.

    Explanation
    ===========
    Beyond the pretty output there is only one other special thing about
    this symbol. ``X.explicit()`` will return the symbolic expression ``X_f -
    X_i`` and add ``X_f`` and ``X_i`` to the recognized symbols in an
    interactive SymPy session.

    After importing the package (``from DeltaSymbol import *``) for an
    interactive session it is recommened that you import SymPy as well:
    ``from sympy import *``. A DeltaSymbol is best created for interactive
    sessions with the ``mkdelta(textname,deltaof)`` call. See the code for
    lower level calls you might make in code.

    Parameters
    ==========
    textname: string for the name of the object, used when calling it in
    python or Sympy expressions (e.g. DX, DG, DeltaT...)
    deltaof: string for the symbol this is delta of (e.g. X, G, T ...)
    **assumptions: any valid assumptions for a symbol. See
    ``sympy.core.symbol``.

    Examples
    ========
    >>> from DeltaSymbol import *
    >>> mkdelta('DG','G')
    >>> DG #In Jupyter this will show the latex typeset version of `\Delta G`
    DG
    >>> DG.explicit()
    G_f - G_i
    >>> from sympy import *
    >>> DG.explicit().subs({G_f:2.0,G_i:1.5})
    0.500000000000000

    """
    def __new__(cls, textname, deltaof, **assumptions):
        cls.name = textname
        cls.basestr = deltaof
        return super().__new__(cls, textname, **assumptions)

    def _repr_latex_(cls):
        return r'$\Delta{' + str(cls.basestr) + '}$'

    def _latex(cls, *obj, **kwargs):
        # mode = kwargs.pop('mode',None)
        # if mode is None:
        #     return latex(cls._repr_latex_(),mode='inline',**kwargs)
        # else:
        return r'\Delta{' + str(cls.basestr) + '}'

    def __str__(cls):
        return cls.name

    def __repr__(cls):
        return cls.__str__()

    def _get_ipython_globals(cls):
        is_not_ipython_global = True
        frame = inspect.currentframe()
        global_dict = frame.f_globals
        try:
            namestr = global_dict['__name__']
            docstr = global_dict['__doc__']
            # print(global_dict['__name__'])
            # print(docstr)
        except KeyError:
            namestr = ''
        if (namestr == '__main__') and (
                docstr == 'Automatically created module for IPython interactive environment'):
            is_not_ipython_global = False
        depth = 0
        try:
            while (is_not_ipython_global):
                nextframe = frame.f_back
                frame = nextframe
                depth += 1
                try:
                    global_dict = frame.f_globals
                    namestr = global_dict['__name__']
                    docstr = global_dict['__doc__']
                    # print(global_dict['__name__'])
                except KeyError:
                    namestr = ''
                if (namestr == '__main__') and (
                        docstr == 'Automatically created module for IPython interactive environment'):
                    is_not_ipython_global = False
        except AttributeError:
            raise AttributeError(
                'Unable to find `__main__` of interactive session. Are you running in Jupyter or IPython?')
        return (global_dict)

    def explicit(cls):
        initstr = cls.basestr + '_i'
        finalstr = cls.basestr + '_f'
        ipyglobals = cls._get_ipython_globals()
        # inject symbols in to ipython global namespace
        ipyglobals[finalstr]= Symbol(finalstr)
        ipyglobals[initstr] = Symbol(initstr)
        return (ipyglobals[finalstr]-ipyglobals[initstr])

def mkdelta(textname, deltaof, **assumptions):
    tmpcls = DeltaSymbol(textname, deltaof, **assumptions)
    ipyglobals = tmpcls._get_ipython_globals()
    ipyglobals[textname]=DeltaSymbol(textname, deltaof, **assumptions)
    return ipyglobals[textname]

DeltaSym = DeltaSymbol
DSym = DeltaSymbol