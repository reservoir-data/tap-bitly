"""Nox configuration."""

from __future__ import annotations

import os
import sys
from textwrap import dedent

import nox

try:
    from nox_poetry import Session, session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.
    Please install it using the following command:
    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None

src_dir = "tap_bitly"
tests_dir = "tests"

python_versions = ["3.11", "3.10", "3.9", "3.8"]
nox.options.sessions = ("tests",)


@session(python=python_versions)
def tests(session: Session) -> None:
    """Execute pytest tests."""
    deps = ["pytest", "pytest-durations"]
    if "GITHUB_ACTIONS" in os.environ:
        deps.append("pytest-github-actions-annotate-failures")

    session.install(".")
    session.install(*deps)
    session.run("pytest", *session.posargs)


@session(name="deps", python=python_versions)
def dependencies(session: Session) -> None:
    """Check issues with dependencies."""
    session.install(".")
    session.install("deptry")
    session.run("deptry", "tap_bitly", *session.posargs)
