# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""Rewrite files, updating occurences of version strings."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import glob
import typing as typ
import difflib
import logging
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import pathlib2 as pl
str = getattr(builtins, 'unicode', str)
from . import parse
from . import config
from . import version
from . import patterns
logger = logging.getLogger('pycalver.rewrite')


def detect_line_sep(content):
    """Parse line separator from content.

    >>> detect_line_sep('\\r\\n')
    '\\r\\n'
    >>> detect_line_sep('\\r')
    '\\r'
    >>> detect_line_sep('\\n')
    '\\n'
    >>> detect_line_sep('')
    '\\n'
    """
    if '\r\n' in content:
        return '\r\n'
    elif '\r' in content:
        return '\r'
    else:
        return '\n'


class NoPatternMatch(Exception):
    """Pattern not found in content.

    logger.error is used to show error info about the patterns so
    that users can debug what is wrong with them. The class
    itself doesn't capture that info. This approach is used so
    that all patter issues can be shown, rather than bubbling
    all the way up the stack on the very first pattern with no
    matches.
    """


def rewrite_lines(pattern_strs, new_vinfo, old_lines):
    """Replace occurances of pattern_strs in old_lines with new_vinfo.

    >>> new_vinfo = version.parse_version_info("v201811.0123-beta")
    >>> pattern_strs = ['__version__ = "{pycalver}"']
    >>> rewrite_lines(pattern_strs, new_vinfo, ['__version__ = "v201809.0002-beta"'])
    ['__version__ = "v201811.0123-beta"']

    >>> pattern_strs = ['__version__ = "{pep440_version}"']
    >>> rewrite_lines(pattern_strs, new_vinfo, ['__version__ = "201809.2b0"'])
    ['__version__ = "201811.123b0"']
    """
    new_lines = old_lines[:]
    found_patterns = set()
    for match in parse.iter_matches(old_lines, pattern_strs):
        found_patterns.add(match.pattern)
        replacement = version.format_version(new_vinfo, match.pattern)
        span_l, span_r = match.span
        new_line = match.line[:span_l] + replacement + match.line[span_r:]
        new_lines[match.lineno] = new_line
    non_matched_patterns = set(pattern_strs) - found_patterns
    if non_matched_patterns:
        for non_matched_pattern in non_matched_patterns:
            logger.error("No match for pattern '{0}'".format(
                non_matched_pattern))
            compiled_pattern_str = patterns.compile_pattern_str(
                non_matched_pattern)
            logger.error("Pattern compiles to regex '{0}'".format(
                compiled_pattern_str))
        raise NoPatternMatch('Invalid pattern(s)')
    else:
        return new_lines


RewrittenFileData = typ.NamedTuple('RewrittenFileData', [('path', str), (
    'line_sep', str), ('old_lines', typ.List[str]), ('new_lines', typ.List[
    str])])


def rfd_from_content(pattern_strs, new_vinfo, content):
    """Rewrite pattern occurrences with version string.

    >>> new_vinfo = version.parse_version_info("v201809.0123")
    >>> pattern_strs = ['__version__ = "{pycalver}"']
    >>> content = '__version__ = "v201809.0001-alpha"'
    >>> rfd = rfd_from_content(pattern_strs, new_vinfo, content)
    >>> rfd.new_lines
    ['__version__ = "v201809.0123"']
    >>>
    >>> new_vinfo = version.parse_version_info("v1.2.3", "v{semver}")
    >>> pattern_strs = ['__version__ = "v{semver}"']
    >>> content = '__version__ = "v1.2.2"'
    >>> rfd = rfd_from_content(pattern_strs, new_vinfo, content)
    >>> rfd.new_lines
    ['__version__ = "v1.2.3"']
    """
    line_sep = detect_line_sep(content)
    old_lines = content.split(line_sep)
    new_lines = rewrite_lines(pattern_strs, new_vinfo, old_lines)
    return RewrittenFileData('<path>', line_sep, old_lines, new_lines)


def _iter_file_paths(file_patterns):
    for globstr, pattern_strs in file_patterns.items():
        file_paths = glob.glob(globstr)
        if not any(file_paths):
            errmsg = "No files found for path/glob '{0}'".format(globstr)
            raise IOError(errmsg)
        for file_path_str in file_paths:
            file_path = pl.Path(file_path_str)
            yield file_path, pattern_strs


def iter_rewritten(file_patterns, new_vinfo):
    """Iterate over files with version string replaced.

    >>> file_patterns = {"src/pycalver/__init__.py": ['__version__ = "{pycalver}"']}
    >>> new_vinfo = version.parse_version_info("v201809.0123")
    >>> rewritten_datas = iter_rewritten(file_patterns, new_vinfo)
    >>> rfd = list(rewritten_datas)[0]
    >>> assert rfd.new_lines == [
    ...     '# This file is part of the pycalver project',
    ...     '# https://gitlab.com/mbarkhau/pycalver',
    ...     '#',
    ...     '# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License',
    ...     '# SPDX-License-Identifier: MIT',
    ...     '""\"PyCalVer: CalVer for Python Packages.""\"',
    ...     '',
    ...     '__version__ = "v201809.0123"',
    ...     '',
    ... ]
    >>>
    """
    fobj = None
    for file_path, pattern_strs in _iter_file_paths(file_patterns):
        with file_path.open(mode='rt', encoding='utf-8') as fobj:
            content = fobj.read()
        rfd = rfd_from_content(pattern_strs, new_vinfo, content)
        yield rfd._replace(path=str(file_path))


def diff_lines(rfd):
    """Generate unified diff.

    >>> rfd = RewrittenFileData(
    ...    path      = "<path>",
    ...    line_sep  = "\\n",
    ...    old_lines = ["foo"],
    ...    new_lines = ["bar"],
    ... )
    >>> diff_lines(rfd)
    ['--- <path>', '+++ <path>', '@@ -1 +1 @@', '-foo', '+bar']
    """
    lines = difflib.unified_diff(a=rfd.old_lines, b=rfd.new_lines, lineterm
        ='', fromfile=rfd.path, tofile=rfd.path)
    return list(lines)


def diff(new_vinfo, file_patterns):
    """Generate diffs of rewritten files.

    >>> new_vinfo = version.parse_version_info("v201809.0123")
    >>> file_patterns = {"src/pycalver/__init__.py": ['__version__ = "{pycalver}"']}
    >>> diff_str = diff(new_vinfo, file_patterns)
    >>> lines = diff_str.split("\\n")
    >>> lines[:2]
    ['--- src/pycalver/__init__.py', '+++ src/pycalver/__init__.py']
    >>> assert lines[6].startswith('-__version__ = "v2')
    >>> assert not lines[6].startswith('-__version__ = "v201809.0123"')
    >>> lines[7]
    '+__version__ = "v201809.0123"'
    """
    full_diff = ''
    fobj = None
    for file_path, pattern_strs in sorted(_iter_file_paths(file_patterns)):
        with file_path.open(mode='rt', encoding='utf-8') as fobj:
            content = fobj.read()
        try:
            rfd = rfd_from_content(pattern_strs, new_vinfo, content)
        except NoPatternMatch:
            errmsg = "No patterns matched for '{0}'".format(file_path)
            raise NoPatternMatch(errmsg)
        rfd = rfd._replace(path=str(file_path))
        lines = diff_lines(rfd)
        if len(lines) == 0:
            errmsg = "No patterns matched for '{0}'".format(file_path)
            raise NoPatternMatch(errmsg)
        full_diff += '\n'.join(lines) + '\n'
    full_diff = full_diff.rstrip('\n')
    return full_diff


def rewrite(file_patterns, new_vinfo):
    """Rewrite project files, updating each with the new version."""
    fobj = None
    for file_data in iter_rewritten(file_patterns, new_vinfo):
        new_content = file_data.line_sep.join(file_data.new_lines)
        with io.open(file_data.path, mode='wt', encoding='utf-8') as fobj:
            fobj.write(new_content)
