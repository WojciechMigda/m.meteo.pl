# -*- coding: utf-8 -*-

import decimal


def floor_to_odd(x: float) -> int:
    # Exactly floor x to an odd integer.
    if not isinstance(x, (float, str, decimal.Decimal)):
        x = float(x)
    if not isinstance(x, (str, decimal.Decimal)):
        x = str(x)
    res = ((decimal.Decimal(x) - 1) // 2) * 2 + 1
    return int(res)


def floor(x: float) -> int:
    # Exactly floor x to an integer.
    if not isinstance(x, (float, str, decimal.Decimal)):
        x = float(x)
    if not isinstance(x, (str, decimal.Decimal)):
        x = str(x)
    res = decimal.Decimal(x) // 1
    return int(res)
