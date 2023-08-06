# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""Functions related to version string manipulation."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import typing as typ
import logging
import datetime as dt
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import pkg_resources
str = getattr(builtins, 'unicode', str)
from . import lex_id
from . import patterns
logger = logging.getLogger('pycalver.version')
TODAY = dt.datetime.utcnow().date()
PATTERN_PART_FIELDS = {'year': 'year', 'month': 'month', 'month_short':
    'month', 'pep440_tag': 'tag', 'tag': 'tag', 'yy': 'year', 'yyyy':
    'year', 'quarter': 'quarter', 'iso_week': 'iso_week', 'us_week':
    'us_week', 'dom': 'dom', 'doy': 'doy', 'dom_short': 'dom', 'doy_short':
    'doy', 'MAJOR': 'major', 'MINOR': 'minor', 'MM': 'minor', 'MMM':
    'minor', 'MMMM': 'minor', 'MMMMM': 'minor', 'PP': 'patch', 'PPP':
    'patch', 'PPPP': 'patch', 'PPPPP': 'patch', 'PATCH': 'patch',
    'build_no': 'bid', 'bid': 'bid', 'BID': 'bid', 'BB': 'bid', 'BBB':
    'bid', 'BBBB': 'bid', 'BBBBB': 'bid', 'BBBBBB': 'bid', 'BBBBBBB': 'bid'}
CalendarInfo = typ.NamedTuple('CalendarInfo', [('year', int), ('quarter',
    int), ('month', int), ('dom', int), ('doy', int), ('iso_week', int), (
    'us_week', int)])


def _date_from_doy(year, doy):
    """Parse date from year and day of year (1 indexed).

    >>> cases = [
    ...     (2016, 1), (2016, 31), (2016, 31 + 1), (2016, 31 + 29), (2016, 31 + 30),
    ...     (2017, 1), (2017, 31), (2017, 31 + 1), (2017, 31 + 28), (2017, 31 + 29),
    ... ]
    >>> dates = [_date_from_doy(year, month) for year, month in cases]
    >>> assert [(d.month, d.day) for d in dates] == [
    ...     (1, 1), (1, 31), (2, 1), (2, 29), (3, 1),
    ...     (1, 1), (1, 31), (2, 1), (2, 28), (3, 1),
    ... ]
    """
    return dt.date(year, 1, 1) + dt.timedelta(days=doy - 1)


def _quarter_from_month(month):
    """Calculate quarter (1 indexed) from month (1 indexed).

    >>> [_quarter_from_month(month) for month in range(1, 13)]
    [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    """
    return (month - 1) // 3 + 1


def cal_info(date=None):
    """Generate calendar components for current date.

    >>> from datetime import date

    >>> c = cal_info(date(2019, 1, 5))
    >>> (c.year, c.quarter, c.month, c.dom, c.doy, c.iso_week, c.us_week)
    (2019, 1, 1, 5, 5, 0, 0)

    >>> c = cal_info(date(2019, 1, 6))
    >>> (c.year, c.quarter, c.month, c.dom, c.doy, c.iso_week, c.us_week)
    (2019, 1, 1, 6, 6, 0, 1)

    >>> c = cal_info(date(2019, 1, 7))
    >>> (c.year, c.quarter, c.month, c.dom, c.doy, c.iso_week, c.us_week)
    (2019, 1, 1, 7, 7, 1, 1)

    >>> c = cal_info(date(2019, 4, 7))
    >>> (c.year, c.quarter, c.month, c.dom, c.doy, c.iso_week, c.us_week)
    (2019, 2, 4, 7, 97, 13, 14)
    """
    if date is None:
        date = TODAY
    kwargs = {'year': date.year, 'quarter': _quarter_from_month(date.month),
        'month': date.month, 'dom': date.day, 'doy': int(date.strftime('%j'
        ), base=10), 'iso_week': int(date.strftime('%W'), base=10),
        'us_week': int(date.strftime('%U'), base=10)}
    return CalendarInfo(**kwargs)


VersionInfo = typ.NamedTuple('VersionInfo', [('year', typ.Optional[int]), (
    'quarter', typ.Optional[int]), ('month', typ.Optional[int]), ('dom',
    typ.Optional[int]), ('doy', typ.Optional[int]), ('iso_week', typ.
    Optional[int]), ('us_week', typ.Optional[int]), ('major', int), (
    'minor', int), ('patch', int), ('bid', str), ('tag', str)])
FieldKey = str
MatchGroupKey = str
MatchGroupStr = str
PatternGroups = typ.Dict[MatchGroupKey, MatchGroupStr]
FieldValues = typ.Dict[FieldKey, MatchGroupStr]


def _parse_field_values(field_values):
    fvals = field_values
    tag = fvals.get('tag')
    if tag is None:
        tag = 'final'
    tag = TAG_ALIASES.get(tag, tag)
    assert tag is not None
    bid = fvals['bid'] if 'bid' in fvals else '0001'
    year = int(fvals['year']) if 'year' in fvals else None
    doy = int(fvals['doy']) if 'doy' in fvals else None
    month = None
    dom = None
    if year and doy:
        date = _date_from_doy(year, doy)
        month = date.month
        dom = date.day
    else:
        month = int(fvals['month']) if 'month' in fvals else None
        dom = int(fvals['dom']) if 'dom' in fvals else None
    iso_week = None
    us_week = None
    if year and month and dom:
        date = dt.date(year, month, dom)
        doy = int(date.strftime('%j'), base=10)
        iso_week = int(date.strftime('%W'), base=10)
        us_week = int(date.strftime('%U'), base=10)
    else:
        iso_week = None
        us_week = None
    quarter = int(fvals['quarter']) if 'quarter' in fvals else None
    if quarter is None and month:
        quarter = _quarter_from_month(month)
    major = int(fvals['major']) if 'major' in fvals else 0
    minor = int(fvals['minor']) if 'minor' in fvals else 0
    patch = int(fvals['patch']) if 'patch' in fvals else 0
    return VersionInfo(year=year, quarter=quarter, month=month, dom=dom,
        doy=doy, iso_week=iso_week, us_week=us_week, major=major, minor=
        minor, patch=patch, bid=bid, tag=tag)


def _is_calver(nfo):
    """Check pattern for any calendar based parts.

    >>> _is_calver(cal_info())
    True

    >>> vnfo = _parse_version_info({'year': "2018", 'month': "11", 'bid': "0018"})
    >>> _is_calver(vnfo)
    True

    >>> vnfo = _parse_version_info({'MAJOR': "1", 'MINOR': "023", 'PATCH': "45"})
    >>> _is_calver(vnfo)
    False
    """
    for field in CalendarInfo._fields:
        maybe_val = getattr(nfo, field, None)
        if isinstance(maybe_val, int):
            return True
    return False


TAG_ALIASES = {'a': 'alpha', 'b': 'beta', 'pre': 'rc'}
PEP440_TAGS = {'alpha': 'a', 'beta': 'b', 'final': '', 'rc': 'rc', 'dev':
    'dev', 'post': 'post'}
VersionInfoKW = typ.Dict[str, typ.Union[str, int, None]]


class PatternError(Exception):
    pass


def _parse_pattern_groups(pattern_groups):
    for part_name in pattern_groups.keys():
        is_valid_part_name = (part_name in patterns.COMPOSITE_PART_PATTERNS or
            part_name in PATTERN_PART_FIELDS)
        if not is_valid_part_name:
            err_msg = "Invalid part '{0}'".format(part_name)
            raise PatternError(err_msg)
    field_value_items = [(field_name, pattern_groups[part_name]) for 
        part_name, field_name in PATTERN_PART_FIELDS.items() if part_name in
        pattern_groups.keys()]
    all_fields = [field_name for field_name, _ in field_value_items]
    unique_fields = set(all_fields)
    duplicate_fields = [f for f in unique_fields if all_fields.count(f) > 1]
    if any(duplicate_fields):
        err_msg = 'Multiple parts for same field {0}.'.format(duplicate_fields)
        raise PatternError(err_msg)
    return dict(field_value_items)


def _parse_version_info(pattern_groups):
    """Parse normalized VersionInfo from groups of a matched pattern.

    >>> vnfo = _parse_version_info({'year': "2018", 'month': "11", 'bid': "0099"})
    >>> (vnfo.year, vnfo.month, vnfo.quarter, vnfo.bid, vnfo.tag)
    (2018, 11, 4, '0099', 'final')

    >>> vnfo = _parse_version_info({'year': "2018", 'doy': "11", 'bid': "099", 'tag': "b"})
    >>> (vnfo.year, vnfo.month, vnfo.dom, vnfo.bid, vnfo.tag)
    (2018, 1, 11, '099', 'beta')

    >>> vnfo = _parse_version_info({'MAJOR': "1", 'MINOR': "23", 'PATCH': "45"})
    >>> (vnfo.major, vnfo.minor, vnfo.patch)
    (1, 23, 45)

    >>> vnfo = _parse_version_info({'MAJOR': "1", 'MMM': "023", 'PPPP': "0045"})
    >>> (vnfo.major, vnfo.minor, vnfo.patch)
    (1, 23, 45)
    """
    field_values = _parse_pattern_groups(pattern_groups)
    return _parse_field_values(field_values)


def parse_version_info(version_str, pattern='{pycalver}'):
    """Parse normalized VersionInfo.

    >>> vnfo = parse_version_info("v201712.0033-beta", pattern="{pycalver}")
    >>> assert vnfo == _parse_version_info({'year': 2017, 'month': 12, 'bid': "0033", 'tag': "beta"})

    >>> vnfo = parse_version_info("1.23.456", pattern="{semver}")
    >>> assert vnfo == _parse_version_info({'MAJOR': "1", 'MINOR': "23", 'PATCH': "456"})
    """
    regex = patterns.compile_pattern(pattern)
    match = regex.match(version_str)
    if match is None:
        err_msg = ("Invalid version string '{0}' for pattern '{1}'/'{2}'".
            format(version_str, pattern, regex.pattern))
        raise PatternError(err_msg)
    return _parse_version_info(match.groupdict())


def is_valid(version_str, pattern='{pycalver}'):
    """Check if a version matches a pattern.

    >>> is_valid("v201712.0033-beta", pattern="{pycalver}")
    True
    >>> is_valid("v201712.0033-beta", pattern="{semver}")
    False
    >>> is_valid("1.2.3", pattern="{semver}")
    True
    >>> is_valid("v201712.0033-beta", pattern="{semver}")
    False
    """
    try:
        parse_version_info(version_str, pattern)
        return True
    except PatternError:
        return False


ID_FIELDS_BY_PART = {'MAJOR': 'major', 'MINOR': 'minor', 'MM': 'minor',
    'MMM': 'minor', 'MMMM': 'minor', 'MMMMM': 'minor', 'MMMMMM': 'minor',
    'MMMMMMM': 'minor', 'PATCH': 'patch', 'PP': 'patch', 'PPP': 'patch',
    'PPPP': 'patch', 'PPPPP': 'patch', 'PPPPPP': 'patch', 'PPPPPPP':
    'patch', 'BID': 'bid', 'BB': 'bid', 'BBB': 'bid', 'BBBB': 'bid',
    'BBBBB': 'bid', 'BBBBBB': 'bid', 'BBBBBBB': 'bid'}


def format_version(vinfo, pattern):
    """Generate version string.

    >>> import datetime as dt
    >>> vinfo = parse_version_info("v201712.0033-beta", pattern="{pycalver}")
    >>> vinfo_a = vinfo._replace(**cal_info(date=dt.date(2017, 1, 1))._asdict())
    >>> vinfo_b = vinfo._replace(**cal_info(date=dt.date(2017, 12, 31))._asdict())
    >>> vinfo_c = vinfo_b._replace(major=1, minor=2, patch=34, tag='final')

    >>> format_version(vinfo_a, pattern="v{yy}.{BID}{release}")
    'v17.33-beta'
    >>> format_version(vinfo_a, pattern="{pep440_version}")
    '201701.33b0'

    >>> format_version(vinfo_a, pattern="{pycalver}")
    'v201701.0033-beta'
    >>> format_version(vinfo_b, pattern="{pycalver}")
    'v201712.0033-beta'

    >>> format_version(vinfo_a, pattern="v{year}w{iso_week}.{BID}{release}")
    'v2017w00.33-beta'
    >>> format_version(vinfo_b, pattern="v{year}w{iso_week}.{BID}{release}")
    'v2017w52.33-beta'

    >>> format_version(vinfo_a, pattern="v{year}d{doy}.{bid}{release}")
    'v2017d001.0033-beta'
    >>> format_version(vinfo_b, pattern="v{year}d{doy}.{bid}{release}")
    'v2017d365.0033-beta'

    >>> format_version(vinfo_c, pattern="v{year}w{iso_week}.{BID}-{tag}")
    'v2017w52.33-final'
    >>> format_version(vinfo_c, pattern="v{year}w{iso_week}.{BID}{release}")
    'v2017w52.33'

    >>> format_version(vinfo_c, pattern="v{MAJOR}.{MINOR}.{PATCH}")
    'v1.2.34'
    >>> format_version(vinfo_c, pattern="v{MAJOR}.{MM}.{PPP}")
    'v1.02.034'
    """
    full_pattern = pattern
    for part_name, full_part_format in patterns.FULL_PART_FORMATS.items():
        full_pattern = full_pattern.replace('{' + part_name + '}',
            full_part_format)
    kwargs = vinfo._asdict()
    tag = vinfo.tag
    if tag == 'final':
        kwargs['release'] = ''
        kwargs['pep440_tag'] = ''
    else:
        kwargs['release'] = '-' + tag
        kwargs['pep440_tag'] = PEP440_TAGS[tag] + '0'
    kwargs['release_tag'] = tag
    year = vinfo.year
    if year:
        kwargs['yy'] = str(year)[-2:]
        kwargs['yyyy'] = year
    kwargs['BID'] = int(vinfo.bid, 10)
    for part_name, field in ID_FIELDS_BY_PART.items():
        val = kwargs[field]
        if part_name.lower() == field.lower():
            if isinstance(val, str):
                kwargs[part_name] = int(val, base=10)
            else:
                kwargs[part_name] = val
        else:
            assert len(set(part_name)) == 1
            padded_len = len(part_name)
            kwargs[part_name] = str(val).zfill(padded_len)
    return full_pattern.format(**kwargs)


def incr(old_version, pattern='{pycalver}', **kwargs):
    release = kwargs.get('release', None)
    major = kwargs.get('major', False)
    minor = kwargs.get('minor', False)
    patch = kwargs.get('patch', False)
    """Increment version string.

    'old_version' is assumed to be a string that matches 'pattern'
    """
    try:
        old_vinfo = parse_version_info(old_version, pattern)
    except PatternError as ex:
        logger.error(str(ex))
        return None
    cur_vinfo = old_vinfo
    cur_cal_nfo = cal_info()
    old_date = old_vinfo.year or 0, old_vinfo.month or 0, old_vinfo.dom or 0
    cur_date = cur_cal_nfo.year, cur_cal_nfo.month, cur_cal_nfo.dom
    if old_date <= cur_date:
        cur_vinfo = cur_vinfo._replace(**cur_cal_nfo._asdict())
    else:
        logger.warning("Version appears to be from the future '{0}'".format
            (old_version))
    cur_vinfo = cur_vinfo._replace(bid=lex_id.next_id(cur_vinfo.bid))
    if major:
        cur_vinfo = cur_vinfo._replace(major=cur_vinfo.major + 1, minor=0,
            patch=0)
    if minor:
        cur_vinfo = cur_vinfo._replace(minor=cur_vinfo.minor + 1, patch=0)
    if patch:
        cur_vinfo = cur_vinfo._replace(patch=cur_vinfo.patch + 1)
    if release:
        cur_vinfo = cur_vinfo._replace(tag=release)
    new_version = format_version(cur_vinfo, pattern)
    if new_version == old_version:
        logger.error('Invalid arguments or pattern, version did not change.')
        return None
    else:
        return new_version


def to_pep440(version):
    """Derive pep440 compliant version string from PyCalVer version string.

    >>> to_pep440("v201811.0007-beta")
    '201811.7b0'
    """
    return str(pkg_resources.parse_version(version))
