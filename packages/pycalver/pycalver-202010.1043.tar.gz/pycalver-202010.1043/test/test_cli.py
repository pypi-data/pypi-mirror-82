# pylint:disable=redefined-outer-name ; pytest fixtures
# pylint:disable=protected-access ; allowed for test code

import os
import time
import shutil
import subprocess as sp

import pytest
import pathlib2 as pl
from click.testing import CliRunner

import pycalver.cli as cli
import pycalver.config as config
import pycalver.patterns as patterns

SETUP_CFG_FIXTURE = """
[metadata]
license_file = LICENSE

[bdist_wheel]
universal = 1
"""

PYCALVER_TOML_FIXTURE = """
"""

PYPROJECT_TOML_FIXTURE = """
[build-system]
requires = ["setuptools", "wheel"]
"""

ENV = {
    'GIT_AUTHOR_NAME'    : "pycalver_tester",
    'GIT_COMMITTER_NAME' : "pycalver_tester",
    'GIT_AUTHOR_EMAIL'   : "pycalver_tester@nowhere.com",
    'GIT_COMMITTER_EMAIL': "pycalver_tester@nowhere.com",
    'HGUSER'             : "pycalver_tester",
    'PATH'               : os.environ['PATH'],
}


def shell(*cmd):
    return sp.check_output(cmd, env=ENV)


@pytest.fixture
def runner(tmpdir):
    runner   = CliRunner(env=ENV)
    orig_cwd = os.getcwd()

    _debug = 0
    if _debug:
        tmpdir = pl.Path("..") / "tmp_test_pycalver_project"
        if tmpdir.exists():
            time.sleep(0.2)
            shutil.rmtree(str(tmpdir))
        tmpdir.mkdir()

    os.chdir(str(tmpdir))

    yield runner

    os.chdir(orig_cwd)

    if not _debug:
        shutil.rmtree(str(tmpdir))


def test_help(runner):
    result = runner.invoke(cli.cli, ['--help', "-vv"])
    assert result.exit_code == 0
    assert "PyCalVer" in result.output
    assert "bump " in result.output
    assert "test " in result.output
    assert "init " in result.output
    assert "show " in result.output


def test_version(runner):
    result = runner.invoke(cli.cli, ['--version', "-vv"])
    assert result.exit_code == 0
    assert " version v20" in result.output
    match = patterns.PYCALVER_RE.search(result.output)
    assert match


def test_incr_default(runner):
    old_version     = "v201701.0999-alpha"
    initial_version = config._initial_version()

    result = runner.invoke(cli.cli, ['test', "-vv", old_version])
    assert result.exit_code == 0
    new_version = initial_version.replace(".0001-alpha", ".11000-alpha")
    assert f"Version: {new_version}\n" in result.output


def test_incr_semver(runner):
    semver_pattern = "{MAJOR}.{MINOR}.{PATCH}"
    old_version    = "0.1.0"
    new_version    = "0.1.1"

    result = runner.invoke(cli.cli, ['test', "-vv", "--patch", old_version, "{semver}"])
    assert result.exit_code == 0
    assert f"Version: {new_version}\n" in result.output

    result = runner.invoke(cli.cli, ['test', "-vv", "--patch", old_version, semver_pattern])
    assert result.exit_code == 0
    assert f"Version: {new_version}\n" in result.output

    old_version = "0.1.1"
    new_version = "0.2.0"

    result = runner.invoke(cli.cli, ['test', "-vv", "--minor", old_version, semver_pattern])
    assert result.exit_code == 0
    assert f"Version: {new_version}\n" in result.output

    old_version = "0.1.1"
    new_version = "1.0.0"

    result = runner.invoke(cli.cli, ['test', "-vv", "--major", old_version, semver_pattern])
    assert result.exit_code == 0
    assert f"Version: {new_version}\n" in result.output


def test_incr_semver_invalid(runner, caplog):
    result = runner.invoke(cli.cli, ['test', "-vv", "--patch", "0.1.1"])
    assert result.exit_code == 1
    assert len(caplog.records) > 0
    log_record = caplog.records[0]
    assert "Invalid version string" in log_record.message
    assert "for pattern '{pycalver}'" in log_record.message


def test_incr_to_beta(runner):
    old_version     = "v201701.0999-alpha"
    initial_version = config._initial_version()

    result = runner.invoke(cli.cli, ['test', old_version, "-vv", "--release", "beta"])
    assert result.exit_code == 0
    new_version = initial_version.replace(".0001-alpha", ".11000-beta")
    assert f"Version: {new_version}\n" in result.output


def test_incr_to_final(runner):
    old_version     = "v201701.0999-alpha"
    initial_version = config._initial_version()

    result = runner.invoke(cli.cli, ['test', old_version, "-vv", "--release", "final"])
    assert result.exit_code == 0
    new_version = initial_version.replace(".0001-alpha", ".11000")
    assert f"Version: {new_version}\n" in result.output


def test_incr_invalid(runner):
    old_version = "v201701.0999-alpha"

    result = runner.invoke(cli.cli, ['test', old_version, "-vv", "--release", "alfa"])
    assert result.exit_code == 1


def _add_project_files(*files):
    if "README.md" in files:
        with pl.Path("README.md").open(mode="wt", encoding="utf-8") as fobj:
            fobj.write(
                """
                Hello World v201701.0002-alpha !
                aka. 201701.2a0 !
            """
            )

    if "setup.cfg" in files:
        with pl.Path("setup.cfg").open(mode="wt", encoding="utf-8") as fobj:
            fobj.write(SETUP_CFG_FIXTURE)

    if "pycalver.toml" in files:
        with pl.Path("pycalver.toml").open(mode="wt", encoding="utf-8") as fobj:
            fobj.write(PYCALVER_TOML_FIXTURE)

    if "pyproject.toml" in files:
        with pl.Path("pyproject.toml").open(mode="wt", encoding="utf-8") as fobj:
            fobj.write(PYPROJECT_TOML_FIXTURE)


def test_nocfg(runner, caplog):
    _add_project_files("README.md")
    result = runner.invoke(cli.cli, ['show', "-vv"])
    assert result.exit_code == 1
    assert any(
        bool("Could not parse configuration. Perhaps try 'pycalver init'." in r.message)
        for r in caplog.records
    )


def test_novcs_nocfg_init(runner, caplog):
    _add_project_files("README.md")
    # dry mode test
    result = runner.invoke(cli.cli, ['init', "-vv", "--dry"])
    assert result.exit_code == 0
    assert not os.path.exists("pycalver.toml")

    # check logging
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == 'WARNING'
    assert "File not found" in log.message

    # non dry mode
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    # check logging
    assert len(caplog.records) == 2
    log = caplog.records[1]
    assert log.levelname == 'WARNING'
    assert "File not found" in log.message

    assert os.path.exists("pycalver.toml")
    with pl.Path("pycalver.toml").open(mode="r", encoding="utf-8") as fobj:
        cfg_content = fobj.read()

    base_str = config.DEFAULT_TOML_BASE_TMPL.format(initial_version=config._initial_version())
    assert base_str                          in cfg_content
    assert config.DEFAULT_TOML_README_MD_STR in cfg_content

    result = runner.invoke(cli.cli, ['show', "-vv"])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440         : {config._initial_version_pep440()}\n" in result.output

    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 1

    # check logging
    assert len(caplog.records) == 3
    log = caplog.records[2]
    assert log.levelname == 'ERROR'
    assert "Configuration already initialized" in log.message


def test_novcs_setupcfg_init(runner):
    _add_project_files("README.md", "setup.cfg")
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    with pl.Path("setup.cfg").open(mode="r", encoding="utf-8") as fobj:
        cfg_content = fobj.read()

    base_str = config.DEFAULT_CONFIGPARSER_BASE_TMPL.format(
        initial_version=config._initial_version()
    )
    assert base_str                                  in cfg_content
    assert config.DEFAULT_CONFIGPARSER_README_MD_STR in cfg_content

    result = runner.invoke(cli.cli, ['show', "-vv"])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440         : {config._initial_version_pep440()}\n" in result.output


def test_novcs_pyproject_init(runner):
    _add_project_files("README.md", "pyproject.toml")
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    with pl.Path("pyproject.toml").open(mode="r", encoding="utf-8") as fobj:
        cfg_content = fobj.read()

    base_str = config.DEFAULT_TOML_BASE_TMPL.format(initial_version=config._initial_version())
    assert base_str                          in cfg_content
    assert config.DEFAULT_TOML_README_MD_STR in cfg_content

    result = runner.invoke(cli.cli, ['show'])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440         : {config._initial_version_pep440()}\n" in result.output


def _vcs_init(vcs, files=("README.md",)):
    assert vcs in ("git", "hg")
    assert not pl.Path(f".{vcs}").exists()
    shell(f"{vcs}", "init")
    assert pl.Path(f".{vcs}").is_dir()

    for filename in files:
        shell(f"{vcs}", "add", filename)

    shell(f"{vcs}", "commit", "-m", "initial commit")


def test_git_init(runner):
    _add_project_files("README.md")
    _vcs_init("git")

    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ['show'])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440         : {config._initial_version_pep440()}\n" in result.output


def test_hg_init(runner):
    _add_project_files("README.md")
    _vcs_init("hg")

    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ['show'])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440         : {config._initial_version_pep440()}\n" in result.output


def test_git_tag_eval(runner):
    _add_project_files("README.md")
    _vcs_init("git")

    # This will set a version that is older than the version tag
    # we set in the vcs, which should take precedence.
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0
    initial_version    = config._initial_version()
    tag_version        = initial_version.replace(".0001-alpha", ".0123-beta")
    tag_version_pep440 = tag_version[1:7] + ".123b0"

    shell("git", "tag", "--annotate", tag_version, "--message", f"bump version to {tag_version}")

    result = runner.invoke(cli.cli, ['show', "-vv"])
    assert result.exit_code == 0
    assert f"Current Version: {tag_version}\n" in result.output
    assert f"PEP440         : {tag_version_pep440}\n" in result.output


def test_hg_tag_eval(runner):
    _add_project_files("README.md")
    _vcs_init("hg")

    # This will set a version that is older than the version tag
    # we set in the vcs, which should take precedence.
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0
    initial_version    = config._initial_version()
    tag_version        = initial_version.replace(".0001-alpha", ".0123-beta")
    tag_version_pep440 = tag_version[1:7] + ".123b0"

    shell("hg", "tag", tag_version, "--message", f"bump version to {tag_version}")

    result = runner.invoke(cli.cli, ['show', "-vv"])
    assert result.exit_code == 0
    assert f"Current Version: {tag_version}\n" in result.output
    assert f"PEP440         : {tag_version_pep440}\n" in result.output


def test_novcs_bump(runner):
    _add_project_files("README.md")

    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ['bump', "-vv"])
    assert result.exit_code == 0

    calver = config._initial_version()[:7]

    with pl.Path("README.md").open() as fobj:
        content = fobj.read()
        assert calver + ".0002-alpha !\n" in content
        assert calver[1:] + ".2a0 !\n" in content

    result = runner.invoke(cli.cli, ['bump', "-vv", "--release", "beta"])
    assert result.exit_code == 0

    with pl.Path("README.md").open() as fobj:
        content = fobj.read()
        assert calver + ".0003-beta !\n" in content
        assert calver[1:] + ".3b0 !\n" in content


def test_git_bump(runner):
    _add_project_files("README.md")
    _vcs_init("git")

    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    shell("git", "add", "pycalver.toml")
    shell("git", "commit", "-m", "initial commit")

    result = runner.invoke(cli.cli, ['bump', "-vv"])
    assert result.exit_code == 0

    calver = config._initial_version()[:7]

    with pl.Path("README.md").open() as fobj:
        content = fobj.read()
        assert calver + ".0002-alpha !\n" in content


def test_hg_bump(runner):
    _add_project_files("README.md")
    _vcs_init("hg")

    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    shell("hg", "add", "pycalver.toml")
    shell("hg", "commit", "-m", "initial commit")

    result = runner.invoke(cli.cli, ['bump', "-vv"])
    assert result.exit_code == 0

    calver = config._initial_version()[:7]

    with pl.Path("README.md").open() as fobj:
        content = fobj.read()
        assert calver + ".0002-alpha !\n" in content


def test_empty_git_bump(runner, caplog):
    shell("git", "init")
    with pl.Path("setup.cfg").open(mode="w") as fobj:
        fobj.write("")
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    with pl.Path("setup.cfg").open(mode="r") as fobj:
        default_cfg_data = fobj.read()

    assert "[pycalver]\n" in default_cfg_data
    assert "\ncurrent_version = " in default_cfg_data
    assert "\n[pycalver:file_patterns]\n" in default_cfg_data
    assert "\nsetup.cfg =\n" in default_cfg_data

    result = runner.invoke(cli.cli, ['bump'])

    assert any(("working directory is not clean" in r.message) for r in caplog.records)
    assert any(("setup.cfg" in r.message) for r in caplog.records)


def test_empty_hg_bump(runner, caplog):
    shell("hg", "init")
    with pl.Path("setup.cfg").open(mode="w") as fobj:
        fobj.write("")
    result = runner.invoke(cli.cli, ['init', "-vv"])
    assert result.exit_code == 0

    with pl.Path("setup.cfg").open(mode="r") as fobj:
        default_cfg_text = fobj.read()

    assert "[pycalver]\n" in default_cfg_text
    assert "\ncurrent_version = " in default_cfg_text
    assert "\n[pycalver:file_patterns]\n" in default_cfg_text
    assert "\nsetup.cfg =\n" in default_cfg_text

    result = runner.invoke(cli.cli, ['bump'])

    assert any(("working directory is not clean" in r.message) for r in caplog.records)
    assert any(("setup.cfg" in r.message) for r in caplog.records)


SETUP_CFG_SEMVER_FIXTURE = """
[metadata]
license_file = LICENSE

[bdist_wheel]
universal = 1

[pycalver]
current_version = "0.1.0"
version_pattern = "{semver}"

[pycalver:file_patterns]
setup.cfg =
    current_version = "{version}"
"""


def test_bump_semver_warning(runner, caplog):
    _add_project_files("README.md")

    with pl.Path("setup.cfg").open(mode="w") as fobj:
        fobj.write(SETUP_CFG_SEMVER_FIXTURE)

    _vcs_init("hg", files=["README.md", "setup.cfg"])

    result = runner.invoke(cli.cli, ['bump', "-vv", "-n", "--dry"])
    assert result.exit_code == 1

    assert any("version did not change" in r.message for r in caplog.records)
    assert any("--major/--minor/--patch required" in r.message for r in caplog.records)

    result = runner.invoke(cli.cli, ['bump', "-vv", "-n", "--dry", "--patch"])
    assert result.exit_code == 0


def test_bump_semver_diff(runner, caplog):
    _add_project_files("README.md")

    with pl.Path("setup.cfg").open(mode="w") as fobj:
        fobj.write(SETUP_CFG_SEMVER_FIXTURE)

    _vcs_init("hg", files=["README.md", "setup.cfg"])

    cases = [("--major", "1.0.0"), ("--minor", "0.2.0"), ("--patch", "0.1.1")]

    for flag, expected in cases:
        result = runner.invoke(cli.cli, ['bump', "-vv", "-n", "--dry", flag])
        assert result.exit_code == 0
        assert len(caplog.records) == 0

        out_lines = set(result.output.splitlines())

        assert "+++ setup.cfg" in out_lines
        assert "-current_version = \"0.1.0\"" in out_lines
        assert f"+current_version = \"{expected}\"" in out_lines
