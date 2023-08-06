# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""Parse setup.cfg or pycalver.cfg files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import typing as typ
import logging
import datetime as dt
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import six
import toml
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import pathlib2 as pl
str = getattr(builtins, 'unicode', str)
from . import version
logger = logging.getLogger('pycalver.config')
Patterns = typ.List[str]
PatternsByGlob = typ.Dict[str, Patterns]
SUPPORTED_CONFIGS = ['setup.cfg', 'pyproject.toml', 'pycalver.toml']
ProjectContext = typ.NamedTuple('ProjectContext', [('path', pl.Path), (
    'config_filepath', pl.Path), ('config_format', str), ('vcs_type', typ.
    Optional[str])])


def init_project_ctx(project_path='.'):
    """Initialize ProjectContext from a path."""
    if isinstance(project_path, pl.Path):
        path = project_path
    elif project_path is None:
        path = pl.Path('.')
    else:
        path = pl.Path(project_path)
    if (path / 'pycalver.toml').exists():
        config_filepath = path / 'pycalver.toml'
        config_format = 'toml'
    elif (path / 'pyproject.toml').exists():
        config_filepath = path / 'pyproject.toml'
        config_format = 'toml'
    elif (path / 'setup.cfg').exists():
        config_filepath = path / 'setup.cfg'
        config_format = 'cfg'
    else:
        config_filepath = path / 'pycalver.toml'
        config_format = 'toml'
    vcs_type = None
    if (path / '.git').exists():
        vcs_type = 'git'
    elif (path / '.hg').exists():
        vcs_type = 'hg'
    else:
        vcs_type = None
    return ProjectContext(path, config_filepath, config_format, vcs_type)


RawConfig = typ.Dict[str, typ.Any]
Config = typ.NamedTuple('Config', [('current_version', str), (
    'version_pattern', str), ('pep440_version', str), ('commit', bool), (
    'tag', bool), ('push', bool), ('file_patterns', PatternsByGlob)])


def _debug_str(cfg):
    cfg_str_parts = ['Config Parsed: Config(', "current_version='{0}'".
        format(cfg.current_version), "version_pattern='{pycalver}'",
        "pep440_version='{0}'".format(cfg.pep440_version), 'commit={0}'.
        format(cfg.commit), 'tag={0}'.format(cfg.tag), 'push={0}'.format(
        cfg.push), 'file_patterns={']
    for filepath, patterns in cfg.file_patterns.items():
        for pattern in patterns:
            cfg_str_parts.append("\n    '{0}': '{1}'".format(filepath, pattern)
                )
    cfg_str_parts += ['\n})']
    return ', '.join(cfg_str_parts)


MaybeConfig = typ.Optional[Config]
MaybeRawConfig = typ.Optional[RawConfig]
FilePatterns = typ.Dict[str, typ.List[str]]


def _parse_cfg_file_patterns(cfg_parser):
    file_patterns = {}
    file_pattern_items = None
    if cfg_parser.has_section('pycalver:file_patterns'):
        file_pattern_items = cfg_parser.items('pycalver:file_patterns')
    else:
        file_pattern_items = []
    for filepath, patterns_str in file_pattern_items:
        patterns = []
        for line in patterns_str.splitlines():
            pattern = line.strip()
            if pattern:
                patterns.append(pattern)
        file_patterns[filepath] = patterns
    return file_patterns


class _ConfigParser(configparser.RawConfigParser):
    """Custom parser, simply to override optionxform behaviour."""

    def optionxform(self, optionstr):
        """Non-xforming (ie. uppercase preserving) override.

        This is important because our option names are actually
        filenames, so case sensitivity is relevant. The default
        behaviour is to do optionstr.lower()
        """
        return optionstr


OptionVal = typ.Union[str, bool, None]
BOOL_OPTIONS = {'commit': False, 'tag': None, 'push': None}


def _parse_cfg(cfg_buffer):
    cfg_parser = _ConfigParser()
    if hasattr(cfg_parser, 'read_file'):
        cfg_parser.read_file(cfg_buffer)
    else:
        cfg_parser.readfp(cfg_buffer)
    if not cfg_parser.has_section('pycalver'):
        raise ValueError('Missing [pycalver] section.')
    raw_cfg = dict(cfg_parser.items('pycalver'))
    for option, default_val in BOOL_OPTIONS.items():
        val = raw_cfg.get(option, default_val)
        if isinstance(val, six.text_type):
            val = val.lower() in ('yes', 'true', '1', 'on')
        raw_cfg[option] = val
    raw_cfg['file_patterns'] = _parse_cfg_file_patterns(cfg_parser)
    return raw_cfg


def _parse_toml(cfg_buffer):
    raw_full_cfg = toml.load(cfg_buffer)
    raw_cfg = raw_full_cfg.get('pycalver', {})
    for option, default_val in BOOL_OPTIONS.items():
        raw_cfg[option] = raw_cfg.get(option, default_val)
    return raw_cfg


def _normalize_file_patterns(raw_cfg):
    """Create consistent representation of file_patterns.

    The result the same, regardless of the config format.
    """
    version_str = raw_cfg['current_version']
    version_pattern = raw_cfg['version_pattern']
    pep440_version = version.to_pep440(version_str)
    file_patterns = None
    if 'file_patterns' in raw_cfg:
        file_patterns = raw_cfg['file_patterns']
    else:
        file_patterns = {}
    for filepath, patterns in list(file_patterns.items()):
        if not os.path.exists(filepath):
            logger.warning('Invalid config, no such file: {0}'.format(filepath)
                )
        normalized_patterns = []
        for pattern in patterns:
            normalized_pattern = pattern.replace('{version}', version_pattern)
            if version_pattern == '{pycalver}':
                normalized_pattern = normalized_pattern.replace(
                    '{pep440_version}', '{pep440_pycalver}')
            elif version_pattern == '{semver}':
                normalized_pattern = normalized_pattern.replace(
                    '{pep440_version}', '{semver}')
            elif '{pep440_version}' in pattern:
                logger.warning("Invalid config, cannot match '{0}' for '{1}'."
                    .format(pattern, filepath))
                logger.warning("No mapping of '{0}' to '{1}'".format(
                    version_pattern, pep440_version))
            normalized_patterns.append(normalized_pattern)
        file_patterns[filepath] = normalized_patterns
    return file_patterns


def _parse_config(raw_cfg):
    """Parse configuration which was loaded from an .ini/.cfg or .toml file."""
    if 'current_version' not in raw_cfg:
        raise ValueError("Missing 'pycalver.current_version'")
    version_str = raw_cfg['current_version']
    version_str = raw_cfg['current_version'] = version_str.strip('\'" ')
    version_pattern = raw_cfg.get('version_pattern', '{pycalver}')
    version_pattern = raw_cfg['version_pattern'] = version_pattern.strip('\'" '
        )
    version.parse_version_info(version_str, version_pattern)
    pep440_version = version.to_pep440(version_str)
    commit = raw_cfg['commit']
    tag = raw_cfg['tag']
    push = raw_cfg['push']
    if tag is None:
        tag = raw_cfg['tag'] = False
    if push is None:
        push = raw_cfg['push'] = False
    if tag and not commit:
        raise ValueError(
            'pycalver.commit = true required if pycalver.tag = true')
    if push and not commit:
        raise ValueError(
            'pycalver.commit = true required if pycalver.push = true')
    file_patterns = _normalize_file_patterns(raw_cfg)
    cfg = Config(current_version=version_str, version_pattern=
        version_pattern, pep440_version=pep440_version, commit=commit, tag=
        tag, push=push, file_patterns=file_patterns)
    logger.debug(_debug_str(cfg))
    return cfg


def _parse_current_version_default_pattern(cfg, raw_cfg_text):
    is_pycalver_section = False
    for line in raw_cfg_text.splitlines():
        if is_pycalver_section and line.startswith('current_version'):
            return line.replace(cfg.current_version, cfg.version_pattern)
        if line.strip() == '[pycalver]':
            is_pycalver_section = True
        elif line and line[0] == '[' and line[-1] == ']':
            is_pycalver_section = False
    raise ValueError('Could not parse pycalver.current_version')


def parse(ctx):
    """Parse config file if available."""
    if not ctx.config_filepath.exists():
        logger.warning('File not found: {0}'.format(ctx.config_filepath))
        return None
    fobj = None
    cfg_path = None
    if ctx.config_filepath.is_absolute():
        cfg_path = str(ctx.config_filepath.relative_to(ctx.path.absolute()))
    else:
        cfg_path = str(ctx.config_filepath)
    raw_cfg = None
    try:
        with ctx.config_filepath.open(mode='rt', encoding='utf-8') as fobj:
            if ctx.config_format == 'toml':
                raw_cfg = _parse_toml(fobj)
            elif ctx.config_format == 'cfg':
                raw_cfg = _parse_cfg(fobj)
            else:
                err_msg = "Invalid config_format='{ctx.config_format}'"
                raise RuntimeError(err_msg)
            cfg = _parse_config(raw_cfg)
            if cfg_path not in cfg.file_patterns:
                fobj.seek(0)
                raw_cfg_text = fobj.read()
                cfg.file_patterns[cfg_path] = [
                    _parse_current_version_default_pattern(cfg, raw_cfg_text)]
        return cfg
    except ValueError as ex:
        logger.warning("Couldn't parse {0}: {1}".format(cfg_path, str(ex)))
        return None


DEFAULT_CONFIGPARSER_BASE_TMPL = (
    """
[pycalver]
current_version = "{initial_version}"
version_pattern = "{{pycalver}}"
commit = True
tag = True
push = True

[pycalver:file_patterns]
"""
    .lstrip())
DEFAULT_CONFIGPARSER_SETUP_CFG_STR = (
    """
setup.cfg =
    current_version = "{version}\"
""".lstrip())
DEFAULT_CONFIGPARSER_SETUP_PY_STR = (
    """
setup.py =
    "{version}"
    "{pep440_version}\"
""".lstrip())
DEFAULT_CONFIGPARSER_README_RST_STR = (
    """
README.rst =
    {version}
    {pep440_version}
""".lstrip())
DEFAULT_CONFIGPARSER_README_MD_STR = (
    """
README.md =
    {version}
    {pep440_version}
""".lstrip())
DEFAULT_TOML_BASE_TMPL = (
    """
[pycalver]
current_version = "{initial_version}"
version_pattern = "{{pycalver}}"
commit = true
tag = true
push = true

[pycalver.file_patterns]
"""
    .lstrip())
DEFAULT_TOML_PYCALVER_STR = (
    """
"pycalver.toml" = [
    'current_version = "{version}"',
]
""".lstrip()
    )
DEFAULT_TOML_PYPROJECT_STR = (
    """
"pyproject.toml" = [
    'current_version = "{version}"',
]
""".
    lstrip())
DEFAULT_TOML_SETUP_PY_STR = (
    """
"setup.py" = [
    "{version}",
    "{pep440_version}",
]
""".lstrip())
DEFAULT_TOML_README_RST_STR = (
    """
"README.rst" = [
    "{version}",
    "{pep440_version}",
]
""".
    lstrip())
DEFAULT_TOML_README_MD_STR = (
    """
"README.md" = [
    "{version}",
    "{pep440_version}",
]
""".lstrip()
    )


def _initial_version():
    return dt.datetime.now().strftime('v%Y%m.0001-alpha')


def _initial_version_pep440():
    return dt.datetime.now().strftime('%Y%m.1a0')


def default_config(ctx):
    """Generate initial default config."""
    fmt = ctx.config_format
    if fmt == 'cfg':
        base_tmpl = DEFAULT_CONFIGPARSER_BASE_TMPL
        default_pattern_strs_by_filename = {'setup.cfg':
            DEFAULT_CONFIGPARSER_SETUP_CFG_STR, 'setup.py':
            DEFAULT_CONFIGPARSER_SETUP_PY_STR, 'README.rst':
            DEFAULT_CONFIGPARSER_README_RST_STR, 'README.md':
            DEFAULT_CONFIGPARSER_README_MD_STR}
    elif fmt == 'toml':
        base_tmpl = DEFAULT_TOML_BASE_TMPL
        default_pattern_strs_by_filename = {'pyproject.toml':
            DEFAULT_TOML_PYPROJECT_STR, 'pycalver.toml':
            DEFAULT_TOML_PYCALVER_STR, 'setup.py':
            DEFAULT_TOML_SETUP_PY_STR, 'README.rst':
            DEFAULT_TOML_README_RST_STR, 'README.md':
            DEFAULT_TOML_README_MD_STR}
    else:
        raise ValueError(
            "Invalid config_format='{0}', must be either 'toml' or 'cfg'.".
            format(fmt))
    cfg_str = base_tmpl.format(initial_version=_initial_version())
    for filename, default_str in default_pattern_strs_by_filename.items():
        if (ctx.path / filename).exists():
            cfg_str += default_str
    has_config_file = any((ctx.path / fn).exists() for fn in SUPPORTED_CONFIGS)
    if not has_config_file:
        if ctx.config_format == 'cfg':
            cfg_str += DEFAULT_CONFIGPARSER_SETUP_CFG_STR
        if ctx.config_format == 'toml':
            cfg_str += DEFAULT_TOML_PYCALVER_STR
    cfg_str += '\n'
    return cfg_str


def write_content(ctx):
    """Update project config file with initial default config."""
    fobj = None
    cfg_content = default_config(ctx)
    if ctx.config_filepath.exists():
        cfg_content = '\n' + cfg_content
    with ctx.config_filepath.open(mode='at', encoding='utf-8') as fobj:
        fobj.write(cfg_content)
    print('Updated {0}'.format(ctx.config_filepath))
