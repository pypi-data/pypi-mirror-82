#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""
CLI module for PyCalVer.

Provided subcommands: show, test, init, bump
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
import typing as typ
import logging
import subprocess as sp
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import click
str = getattr(builtins, 'unicode', str)
from . import vcs
from . import config
from . import rewrite
from . import version
_VERBOSE = 0
try:
    import pretty_traceback
    pretty_traceback.install()
except ImportError:
    pass
click.disable_unicode_literals_warning = True
VALID_RELEASE_VALUES = 'alpha', 'beta', 'dev', 'rc', 'post', 'final'
logger = logging.getLogger('pycalver.cli')


def _configure_logging(verbose=0):
    if verbose >= 2:
        log_format = (
            '%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-17s - %(message)s'
            )
        log_level = logging.DEBUG
    elif verbose == 1:
        log_format = '%(levelname)-7s - %(message)s'
        log_level = logging.INFO
    else:
        log_format = '%(levelname)-7s - %(message)s'
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format=log_format, datefmt=
        '%Y-%m-%dT%H:%M:%S')
    logger.debug('Logging configured.')


def _validate_release_tag(release):
    if release in VALID_RELEASE_VALUES:
        return
    logger.error('Invalid argument --release={0}'.format(release))
    logger.error('Valid arguments are: {0}'.format(', '.join(
        VALID_RELEASE_VALUES)))
    sys.exit(1)


@click.group()
@click.version_option(version='v202010.1043')
@click.help_option()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
def cli(verbose=0):
    """Automatically update PyCalVer version strings on python projects."""
    global _VERBOSE
    _VERBOSE = verbose


@cli.command()
@click.argument('old_version')
@click.argument('pattern', default='{pycalver}')
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('--release', default=None, metavar='<name>', help=
    'Override release name of current_version')
@click.option('--major', is_flag=True, default=False, help=
    'Increment major component.')
@click.option('--minor', is_flag=True, default=False, help=
    'Increment minor component.')
@click.option('--patch', is_flag=True, default=False, help=
    'Increment patch component.')
def test(old_version, pattern='{pycalver}', verbose=0, release=None, major=
    False, minor=False, patch=False):
    """Increment a version number for demo purposes."""
    _configure_logging(verbose=max(_VERBOSE, verbose))
    if release:
        _validate_release_tag(release)
    new_version = version.incr(old_version, pattern=pattern, release=
        release, major=major, minor=minor, patch=patch)
    if new_version is None:
        logger.error("Invalid version '{0}' and/or pattern '{1}'.".format(
            old_version, pattern))
        sys.exit(1)
    pep440_version = version.to_pep440(new_version)
    click.echo('New Version: {0}'.format(new_version))
    click.echo('PEP440     : {0}'.format(pep440_version))


def _update_cfg_from_vcs(cfg, fetch):
    try:
        vcs_api = vcs.get_vcs_api()
        logger.debug('vcs found: {0}'.format(vcs_api.name))
        if fetch:
            logger.info(
                'fetching tags from remote (to turn off use: -n / --no-fetch)')
            vcs_api.fetch()
        version_tags = [tag for tag in vcs_api.ls_tags() if version.
            is_valid(tag, cfg.version_pattern)]
        if version_tags:
            version_tags.sort(reverse=True)
            logger.debug('found {0} tags: {1}'.format(len(version_tags),
                version_tags[:2]))
            latest_version_tag = version_tags[0]
            latest_version_pep440 = version.to_pep440(latest_version_tag)
            if latest_version_tag > cfg.current_version:
                logger.info('Working dir version        : {0}'.format(cfg.
                    current_version))
                logger.info('Latest version from {0:>3} tag: {1}'.format(
                    vcs_api.name, latest_version_tag))
                cfg = cfg._replace(current_version=latest_version_tag,
                    pep440_version=latest_version_pep440)
        else:
            logger.debug('no vcs tags found')
    except OSError:
        logger.debug('No vcs found')
    return cfg


@cli.command()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('-f/-n', '--fetch/--no-fetch', is_flag=True, default=True,
    help='Sync tags from remote origin.')
def show(verbose=0, fetch=True):
    """Show current version."""
    _configure_logging(verbose=max(_VERBOSE, verbose))
    ctx = config.init_project_ctx(project_path='.')
    cfg = config.parse(ctx)
    if cfg is None:
        logger.error(
            "Could not parse configuration. Perhaps try 'pycalver init'.")
        sys.exit(1)
    cfg = _update_cfg_from_vcs(cfg, fetch=fetch)
    click.echo('Current Version: {0}'.format(cfg.current_version))
    click.echo('PEP440         : {0}'.format(cfg.pep440_version))


@cli.command()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('--dry', default=False, is_flag=True, help=
    "Display diff of changes, don't rewrite files.")
def init(verbose=0, dry=False):
    """Initialize [pycalver] configuration."""
    _configure_logging(verbose=max(_VERBOSE, verbose))
    ctx = config.init_project_ctx(project_path='.')
    cfg = config.parse(ctx)
    if cfg:
        logger.error('Configuration already initialized in {0}'.format(ctx.
            config_filepath))
        sys.exit(1)
    if dry:
        click.echo("Exiting because of '--dry'. Would have written to {0}:"
            .format(ctx.config_filepath))
        cfg_text = config.default_config(ctx)
        click.echo('\n    ' + '\n    '.join(cfg_text.splitlines()))
        sys.exit(0)
    config.write_content(ctx)


def _assert_not_dirty(vcs_api, filepaths, allow_dirty):
    dirty_files = vcs_api.status(required_files=filepaths)
    if dirty_files:
        logger.warning(
            '{0} working directory is not clean. Uncomitted file(s):'.
            format(vcs_api.name))
        for dirty_file in dirty_files:
            logger.warning('    ' + dirty_file)
    if not allow_dirty and dirty_files:
        sys.exit(1)
    dirty_pattern_files = set(dirty_files) & filepaths
    if dirty_pattern_files:
        logger.error('Not commiting when pattern files are dirty:')
        for dirty_file in dirty_pattern_files:
            logger.warning('    ' + dirty_file)
        sys.exit(1)


def _commit(cfg, new_version, vcs_api, filepaths):
    for filepath in filepaths:
        vcs_api.add(filepath)
    vcs_api.commit('bump version to {0}'.format(new_version))
    if cfg.commit and cfg.tag:
        vcs_api.tag(new_version)
    if cfg.commit and cfg.tag and cfg.push:
        vcs_api.push(new_version)


def _bump(cfg, new_version, allow_dirty=False):
    vcs_api = None
    if cfg.commit:
        try:
            vcs_api = vcs.get_vcs_api()
        except OSError:
            logger.warning('Version Control System not found, aborting commit.'
                )
    filepaths = set(cfg.file_patterns.keys())
    if vcs_api:
        _assert_not_dirty(vcs_api, filepaths, allow_dirty)
    try:
        new_vinfo = version.parse_version_info(new_version, cfg.version_pattern
            )
        rewrite.rewrite(cfg.file_patterns, new_vinfo)
    except Exception as ex:
        logger.error(str(ex))
        sys.exit(1)
    if vcs_api:
        _commit(cfg, new_version, vcs_api, filepaths)


def _try_bump(cfg, new_version, allow_dirty=False):
    try:
        _bump(cfg, new_version, allow_dirty)
    except sp.CalledProcessError as ex:
        logger.error('Error running subcommand: {0}'.format(ex.cmd))
        if ex.stdout:
            sys.stdout.write(ex.stdout.decode('utf-8'))
        if ex.stderr:
            sys.stderr.write(ex.stderr.decode('utf-8'))
        sys.exit(1)


def _print_diff(cfg, new_version):
    new_vinfo = version.parse_version_info(new_version, cfg.version_pattern)
    diff = rewrite.diff(new_vinfo, cfg.file_patterns)
    if sys.stdout.isatty():
        for line in diff.splitlines():
            if line.startswith('+++') or line.startswith('---'):
                click.echo(line)
            elif line.startswith('+'):
                click.echo('\x1b[32m' + line + '\x1b[0m')
            elif line.startswith('-'):
                click.echo('\x1b[31m' + line + '\x1b[0m')
            elif line.startswith('@'):
                click.echo('\x1b[36m' + line + '\x1b[0m')
            else:
                click.echo(line)
    else:
        click.echo(diff)


def _try_print_diff(cfg, new_version):
    try:
        _print_diff(cfg, new_version)
    except Exception as ex:
        logger.error(str(ex))
        sys.exit(1)


@cli.command()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('-f/-n', '--fetch/--no-fetch', is_flag=True, default=True,
    help='Sync tags from remote origin.')
@click.option('--dry', default=False, is_flag=True, help=
    "Display diff of changes, don't rewrite files.")
@click.option('--release', default=None, metavar='<name>', help=
    'Override release name of current_version. Valid options are: {0}.'.
    format(', '.join(VALID_RELEASE_VALUES)))
@click.option('--allow-dirty', default=False, is_flag=True, help=
    'Commit even when working directory is has uncomitted changes. (WARNING: The commit will still be aborted if there are uncomitted to files with version strings.'
    )
@click.option('--major', is_flag=True, default=False, help=
    'Increment major component.')
@click.option('--minor', is_flag=True, default=False, help=
    'Increment minor component.')
@click.option('--patch', is_flag=True, default=False, help=
    'Increment patch component.')
def bump(release=None, verbose=0, dry=False, allow_dirty=False, fetch=True,
    major=False, minor=False, patch=False):
    """Increment the current version string and update project files."""
    verbose = max(_VERBOSE, verbose)
    _configure_logging(verbose)
    if release:
        _validate_release_tag(release)
    ctx = config.init_project_ctx(project_path='.')
    cfg = config.parse(ctx)
    if cfg is None:
        logger.error(
            "Could not parse configuration. Perhaps try 'pycalver init'.")
        sys.exit(1)
    cfg = _update_cfg_from_vcs(cfg, fetch=fetch)
    old_version = cfg.current_version
    new_version = version.incr(old_version, pattern=cfg.version_pattern,
        release=release, major=major, minor=minor, patch=patch)
    if new_version is None:
        is_semver = '{semver}' in cfg.version_pattern
        has_semver_inc = major or minor or patch
        if is_semver and not has_semver_inc:
            logger.warning(
                'bump --major/--minor/--patch required when using semver.')
        else:
            logger.error("Invalid version '{0}' and/or pattern '{1}'.".
                format(old_version, cfg.version_pattern))
        sys.exit(1)
    logger.info('Old Version: {0}'.format(old_version))
    logger.info('New Version: {0}'.format(new_version))
    if dry or verbose >= 2:
        _try_print_diff(cfg, new_version)
    if dry:
        return
    _try_bump(cfg, new_version, allow_dirty)


if __name__ == '__main__':
    cli()
