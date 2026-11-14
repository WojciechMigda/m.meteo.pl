# -*- coding: utf-8 -*-

import sys
import plac
import math
import decimal


def plac_call(obj, arglist=None, eager=True, version=None):
    """
    If obj is a function or a bound method, parse the given arglist
    by using the parser inferred from the annotations of obj
    and call obj with the parsed arguments.
    If obj is an object with attribute .commands, dispatch to the
    associated subparser.
    """
    if arglist is None:
        arglist = sys.argv[1:]
    parser = plac.parser_from(obj)
    parser.add_argument(
        '--version', '-V', action='version', version=version)
    cmd, result = parser.consume(arglist)
    if plac.iterable(result) and eager:  # listify the result
        return list(result)
    return result


def comma_set(arg: str) -> set[str]:
    '''Do użycia jako konstruktor w specyfikacji argumentu `plac`, np.
arg: ("Argument.", 'option', 'a', libplac.comma_set),

Wtedy przekazany `arg` będzie rozparsowany do typu set[str].
'''
    return {token.strip() for token in arg.split(',')}


def comma_list(arg: str) -> list[str]:
    '''Do użycia jako konstruktor w specyfikacji argumentu `plac`, np.
arg: ("Argument.", 'option', 'a', libplac.comma_list),

Wtedy przekazany `arg` będzie rozparsowany do typu list[str].
'''
    return [token.strip() for token in arg.split(',')]


def positive_int(arg: str) -> int:
    '''Parse plac argument asserting it is a positive integer.
    '''
    rv = int(arg)
    if rv <= 0: raise ValueError(f"argument {rv} is not a positive integer")
    return rv


def nonnegative_int(arg: str) -> int:
    '''Parse plac argument asserting it is a non-negative integer.
    '''
    rv = int(arg)
    if rv < 0: raise ValueError(f"argument {rv} is not a non-negative integer")
    return rv


def negative_int(arg: str) -> int:
    '''Parse plac argument asserting it is a negative integer.
    '''
    rv = int(arg)
    if rv >= 0: raise ValueError(f"argument {rv} is not a negative integer")
    return rv


def __normal_float(v: float) -> bool:
    # Predicate to test if float is a normal number
    return math.isfinite(v) and not math.isnan(v)


def positive_float(arg: str) -> float:
    '''Parse plac argument asserting it is a positive float.
    '''
    rv = float(arg)
    if not __normal_float(rv) or rv <= 0.0: raise ValueError(f"argument {rv} is not a positive float")
    return rv


def nonnegative_float(arg: str) -> float:
    '''Parse plac argument asserting it is a non-negative float.
    '''
    rv = float(arg)
    if not __normal_float(rv) or rv < 0: raise ValueError(f"argument {rv} is not a non-negative float")
    return rv


def negative_float(arg: str) -> float:
    '''Parse plac argument asserting it is a negative float.
    '''
    rv = float(arg)
    if not __normal_float(rv) or rv >= 0: raise ValueError(f"argument {rv} is not a negative float")
    return rv


def positive_decimal(arg: str) -> decimal.Decimal:
    '''Parse plac argument asserting it is a positive decimal.Decimal.
    '''
    rv = decimal.Decimal(arg)
    if not rv.is_finite() or rv <= 0.0: raise ValueError(f"argument {rv} is not a positive number")
    return rv


def nonnegative_decimal(arg: str) -> decimal.Decimal:
    '''Parse plac argument asserting it is a non-negative decimal.Decimal.
    '''
    rv = decimal.Decimal(arg)
    if not rv.is_finite() or rv < 0: raise ValueError(f"argument {rv} is not a non-negative number")
    return rv


def negative_decimal(arg: str) -> decimal.Decimal:
    '''Parse plac argument asserting it is a negative decimal.Decimal.
    '''
    rv = decimal.Decimal(arg)
    if not rv.is_finite() or rv >= 0: raise ValueError(f"argument {rv} is not a negative number")
    return rv


__all__ = [
    "plac_call",
    "comma_set",
    "comma_list",
    "positive_int",
    "nonnegative_int",
    "negative_int",
    "positive_float",
    "nonnegative_float",
    "negative_float",
    "positive_decimal",
    "nonnegative_decimal",
    "negative_decimal",
]
