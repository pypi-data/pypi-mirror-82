import re

import pytest

from pycalver import patterns


def _part_re_by_name(name):
    return re.compile(patterns.PART_PATTERNS[name])


@pytest.mark.parametrize("part_name", patterns.PART_PATTERNS.keys())
def test_part_compilation(part_name):
    assert _part_re_by_name(part_name)


PATTERN_PART_CASES = [
    ("pep440_pycalver", "201712.31"          , "201712.31"),
    ("pep440_pycalver", "v201712.0032"       , None),
    ("pep440_pycalver", "201712.0033-alpha"  , None),
    ("pycalver"       , "v201712.0034"       , "v201712.0034"),
    ("pycalver"       , "v201712.0035-alpha" , "v201712.0035-alpha"),
    ("pycalver"       , "v201712.0036-alpha0", "v201712.0036-alpha"),
    ("pycalver"       , "v201712.0037-pre"   , "v201712.0037"),
    ("pycalver"       , "201712.38a0"        , None),
    ("pycalver"       , "201712.0039"        , None),
    ("semver"         , "1.23.456"           , "1.23.456"),
    ("calver"         , "v201712"            , "v201712"),
    ("calver"         , "v201799"            , None),  # invalid date
    ("calver"         , "201712"             , None),
    ("calver"         , "v20171"             , None),
    ("build"          , ".0012"              , ".0012"),
    ("build"          , ".11012"             , ".11012"),
    ("build"          , ".012"               , None),
    ("build"          , "11012"              , None),
    ("release"        , "-alpha"             , "-alpha"),
    ("release"        , "-beta"              , "-beta"),
    ("release"        , "-dev"               , "-dev"),
    ("release"        , "-rc"                , "-rc"),
    ("release"        , "-post"              , "-post"),
    ("release"        , "-pre"               , ""),
    ("release"        , "alpha"              , ""),
]


@pytest.mark.parametrize("part_name, line, expected", PATTERN_PART_CASES)
def test_re_pattern_parts(part_name, line, expected):
    part_re = _part_re_by_name(part_name)
    result  = part_re.search(line)
    if result is None:
        assert expected is None, (part_name, line)
    else:
        result_val = result.group(0)
        assert result_val == expected, (part_name, line)


PATTERN_CASES = [
    (r"v{year}.{month}.{MINOR}"      , "v2017.11.1" , "v2017.11.1"),
    (r"v{year}.{month}.{MINOR}"      , "v2017.07.12", "v2017.07.12"),
    (r"v{year}.{month_short}.{MINOR}", "v2017.11.1" , "v2017.11.1"),
    (r"v{year}.{month_short}.{MINOR}", "v2017.7.12" , "v2017.7.12"),
]


@pytest.mark.parametrize("pattern_str, line, expected", PATTERN_CASES)
def test_patterns(pattern_str, line, expected):
    pattern_re = patterns.compile_pattern(pattern_str)
    result     = pattern_re.search(line)
    if result is None:
        assert expected is None, (pattern_str, line)
    else:
        result_val = result.group(0)
        assert result_val == expected, (pattern_str, line)


CLI_MAIN_FIXTURE = """
@click.group()
@click.version_option(version="v201812.0123-beta")
@click.help_option()
"""


def test_pattern_escapes():
    pattern    = 'click.version_option(version="{pycalver}")'
    pattern_re = patterns.compile_pattern(pattern)
    match      = pattern_re.search(CLI_MAIN_FIXTURE)
    expected   = 'click.version_option(version="v201812.0123-beta")'
    assert match.group(0) == expected


CURLY_BRACE_FIXTURE = """
package_metadata = {"name": "mypackage", "version": "v201812.0123-beta"}
"""


def test_curly_escapes():
    pattern    = 'package_metadata = {"name": "mypackage", "version": "{pycalver}"}'
    pattern_re = patterns.compile_pattern(pattern)
    match      = pattern_re.search(CURLY_BRACE_FIXTURE)
    expected   = 'package_metadata = {"name": "mypackage", "version": "v201812.0123-beta"}'
    assert match.group(0) == expected
