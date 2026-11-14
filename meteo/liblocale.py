# -*- coding: utf-8 -*-

import contextlib
import locale


@contextlib.contextmanager
def temporary_locale(category: int, loc: str | tuple[str | None, str | None]):
    old_locale = locale.getlocale(category)
    try:
        locale.setlocale(category, loc)
        yield
    finally:
        locale.setlocale(category, old_locale)
