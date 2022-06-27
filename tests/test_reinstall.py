import sys

import pytest  # type: ignore

from helpers import WIN, mock_legacy_venv, run_pipx_cli
from pipx import emojis


def test_reinstall(pipx_temp_env, capsys):
    assert not run_pipx_cli(["install", "pycowsay"])
    assert not run_pipx_cli(["reinstall", "--python", sys.executable, "pycowsay"])


def test_reinstall_shared(pipx_temp_env, monkeypatch, capfd):
    if WIN:
        monkeypatch.setattr(emojis, "EMOJI_SUPPORT", False)
    with capfd.disabled():
        assert not run_pipx_cli(["install", "--shared", "pycowsay"])
        assert not run_pipx_cli(["reinstall", "--python", sys.executable, "pycowsay"])

    assert not run_pipx_cli(["runpip", "--shared", "freeze"])
    captured = capfd.readouterr()
    assert captured.out.startswith("pycowsay==")


def test_reinstall_nonexistent(pipx_temp_env, capsys):
    assert run_pipx_cli(["reinstall", "--python", sys.executable, "nonexistent"])
    assert "Nothing to reinstall for nonexistent" in capsys.readouterr().out


@pytest.mark.parametrize("metadata_version", [None, "0.1"])
def test_reinstall_legacy_venv(pipx_temp_env, capsys, metadata_version):
    assert not run_pipx_cli(["install", "pycowsay"])
    mock_legacy_venv("pycowsay", metadata_version=metadata_version)

    assert not run_pipx_cli(["reinstall", "--python", sys.executable, "pycowsay"])


def test_reinstall_suffix(pipx_temp_env, capsys):
    suffix = "_x"
    assert not run_pipx_cli(["install", "pycowsay", f"--suffix={suffix}"])

    assert not run_pipx_cli(
        ["reinstall", "--python", sys.executable, f"pycowsay{suffix}"]
    )


@pytest.mark.parametrize("metadata_version", ["0.1"])
def test_reinstall_suffix_legacy_venv(pipx_temp_env, capsys, metadata_version):
    suffix = "_x"
    assert not run_pipx_cli(["install", "pycowsay", f"--suffix={suffix}"])
    mock_legacy_venv(f"pycowsay{suffix}", metadata_version=metadata_version)

    assert not run_pipx_cli(
        ["reinstall", "--python", sys.executable, f"pycowsay{suffix}"]
    )


def test_reinstall_specifier(pipx_temp_env, capsys):
    assert not run_pipx_cli(["install", "pylint==2.3.1"])

    # clear capsys before reinstall
    captured = capsys.readouterr()

    assert not run_pipx_cli(["reinstall", "--python", sys.executable, "pylint"])
    captured = capsys.readouterr()
    assert "installed package pylint 2.3.1" in captured.out
