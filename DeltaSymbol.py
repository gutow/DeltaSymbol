from sympy.core.symbol import Symbol
import inspect


class DeltaSymbol(Symbol):
    """
    This class extends SymPy symbols to include Delta of a symbol ``X`` which
    is displayed as typeset latex in Jupyter notebooks and a user chosen
    python compatible character sequence in plain text.

    Explanation
    ===========
    Beyond the pretty output there is only one other special thing about
    this symbol. ``X.explicit`` will return the symbolic expression ``X_f -
    X_i`` and add ``X_f`` and ``X_i`` to the recognized symbols in an
    interactive SymPy session.

    After importing the package (``from DeltaSymbol import *``) for an
    interactive session it is recommened that you import SymPy as well:
    ``from sympy import *``. A DeltaSymbol is best created for interactive
    sessions with a statement like: ``DX = mkdelta('X')`` call.
    ``DeltaSymbol()``, ``DeltaSym()`` and ``DSym()``are all synonyms for
    ``mkdelta()``.

    Parameters
    ==========
    deltaof: string for the symbol this is delta of (e.g. 'X', 'G', 'T' ...)
    or an existing sympy Symbol (e.g. X or T).
    **assumptions: any valid assumptions for a symbol. See
    ``sympy.core.symbol``.

    Examples
    ========
    >>> from DeltaSymbol import mkdelta
    >>> DG = mkdelta('G')
    >>> DG # In Jupyter this will show the latex typeset version of `\Delta G`
    \Delta G
    >>> # Below only works in IPython/Jupyter
    >>> DG.explicit # doctest: +SKIP
    G_f - G_i
    >>> DG.explicit().subs({G_f:2.0,G_i:1.5}) # doctest: +SKIP
    0.500000000000000
    >>> T = Symbol('T')
    >>> DT = mkdelta(T)
    >>> DT
    \Delta T

    """

    def __new__(cls, deltaof, **assumptions):
        # obj = super().__new__(cls, textname, **assumptions)
        cls.basestr = str(deltaof)
        cls.latexstr = r'\Delta ' + cls.basestr
        return super().__new__(cls, cls.latexstr, **assumptions)

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

    @property
    def explicit(cls):
        from sympy.core.sympify import sympify
        stri = cls.basestr + '_i'
        strf = cls.basestr + '_f'
        ipg = cls._get_ipython_globals()
        ipg[stri] = Symbol(stri)
        ipg[strf] = Symbol(strf)
        return sympify(strf + '-' + stri)


mkdelta = DeltaSymbol
DSym = DeltaSymbol
DeltaSym = DeltaSymbol