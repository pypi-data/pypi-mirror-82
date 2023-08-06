# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""Parse PyCalVer strings from files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import typing as typ
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
from .patterns import compile_pattern
str = getattr(builtins, 'unicode', str)
PatternMatch = typ.NamedTuple('PatternMatch', [('lineno', int), ('line',
    str), ('pattern', str), ('span', typ.Tuple[int, int]), ('match', str)])
PatternMatches = typ.Iterable[PatternMatch]


def _iter_for_pattern(lines, pattern):
    pattern_re = compile_pattern(pattern)
    for lineno, line in enumerate(lines):
        match = pattern_re.search(line)
        if match:
            yield PatternMatch(lineno, line, pattern, match.span(), match.
                group(0))


def iter_matches(lines, patterns):
    """Iterate over all matches of any pattern on any line.

    >>> lines = ["__version__ = 'v201712.0002-alpha'"]
    >>> patterns = ["{pycalver}", "{pep440_pycalver}"]
    >>> matches = list(iter_matches(lines, patterns))
    >>> assert matches[0] == PatternMatch(
    ...     lineno = 0,
    ...     line   = "__version__ = 'v201712.0002-alpha'",
    ...     pattern= "{pycalver}",
    ...     span   = (15, 33),
    ...     match  = "v201712.0002-alpha",
    ... )
    """
    for pattern in patterns:
        for match in _iter_for_pattern(lines, pattern):
            yield match
