import inspect
from collections.abc import Sequence

import nox

# -------------------------
# config
# -------------------------

nox.options.default_venv_backend = "uv"
nox.options.stop_on_first_error = True

# Standard sessions to run
nox.options.sessions = [
    "tests_scripts",
    "tests_scripts_ui",
    "tests_ui",
]

PYTHON_VERSIONS: list[str] = ["3.9", "3.12"]
PYTHON_VERSIONS_LATEST: list[str] = ["3.12"]

FLET_VERSION_OLD: list[str] = ["0.27.*", "0.28.*"]
FLET_VERSIONS_NEW: list[str] = ["0.80.*", "0.82.*", "0.83.*", "0.84.0"]
FLET_VERSION_LATEST: str = "0.84.0"
FLET_VERSIONS_ALL: list[str] = FLET_VERSION_OLD + FLET_VERSIONS_NEW


_PYTEST: list[str] = [
    "pytest",
    "-q",
    "-s",
    "--tb=short",
]


def _install_base(session: nox.Session, flet_version: str) -> None:
    """Installs the base dependencies for testing."""
    session.log(f"Installing flet=={flet_version} on Python {session.python}")

    session.install(
        ".[jwt]",
        f"flet[all]=={flet_version}",
        "pytest",
        "pytest-asyncio",
        "anyio",
        "pytest-cov",
        "tortoise-orm>=0.22.2",
        "sqlmodel>=0.0.24",
    )


def _skip(session: nox.Session, version: str) -> bool:
    """Checks if a session should be skipped based on version compatibility."""
    return session.python == "3.9" and version in FLET_VERSIONS_NEW


# tests scripts result storage
result_tests: dict[str, str] = {}


class Test:
    """Helper class to manage and report test results."""

    def __init__(self, session: nox.Session, name_function: str) -> None:
        self.session: nox.Session = session
        self.name_function: str = name_function
        self.message: str = f"\n--------- [flet-easy tests - {name_function}] ---------\n"

    def run(self, file_path: str, flet_version: str, ui: bool = False) -> None:
        """Runs a test file and logs the outcome."""
        self.session.log(f"py: {self.session.python} - flet: {flet_version} - test: {file_path}")

        # Choose the command based on UI flag
        cmd: Sequence[str] = ["flet", "run"] if ui else _PYTEST

        env = dict(self.session.env)
        env["PYTHONIOENCODING"] = "utf-8"

        self.session.run(
            *cmd,
            file_path,
            env=env,
        )
        self._finish_test(file_path, flet_version)

    def _finish_test(self, message: str, flet_version: str) -> None:
        """Internal helper to log the end of a test run."""
        self.session.log(f"Finish: py: {self.session.python} - flet: {flet_version} - {message}")
        self.message += f"✅ Finish: py: {self.session.python} - flet: {flet_version} - {message}\n"

    def finish(self, all: bool = False) -> None:
        """Reports the final results to the session log."""
        if all:
            return self.session.log("\n".join(result_tests.values()))

        if result_tests.get(self.name_function):
            result_tests[self.name_function] += self.message
        else:
            result_tests[self.name_function] = self.message

        self.session.log(result_tests[self.name_function])


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def tests_scripts(session: nox.Session):
    """tests scripts"""

    test = Test(session, inspect.currentframe().f_code.co_name)

    for flet_version in FLET_VERSIONS_ALL:
        if _skip(session, flet_version):
            continue

        print(flet_version)
        _install_base(session, flet_version)

        if flet_version in FLET_VERSIONS_NEW:
            test.run("tests/routing_decorator.py", flet_version)
            test.run("tests/routing-pagesy.py", flet_version)

        # sharedPreferences
        test.run("tests/shared_preferences.py", flet_version)

        # middlewares
        test.run("tests/middlewares.py", flet_version)

        # params
        test.run("tests/routing_parameters.py", flet_version)

    test.finish()


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def tests_scripts_ui(session: nox.Session):
    """tests scripts ui"""

    test = Test(session, inspect.currentframe().f_code.co_name)

    for flet_version in FLET_VERSIONS_ALL:
        if _skip(session, flet_version):
            continue

        _install_base(session, flet_version)

        if flet_version in FLET_VERSIONS_NEW:
            test.run("tests/ui/routing_decorator.py", flet_version, ui=True)
            test.run("tests/ui/routing-pagesy.py", flet_version, ui=True)

        # sharedPreferences
        test.run("tests/ui/shared_preferences.py", flet_version, ui=True)

        # middlewares
        test.run("tests/ui/middlewares.py", flet_version, ui=True)

    test.finish()


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def tests_ui(session: nox.Session):
    """tests ui"""

    test = Test(session, inspect.currentframe().f_code.co_name)

    for flet_version in FLET_VERSIONS_ALL:
        if _skip(session, flet_version):
            continue

        _install_base(session, flet_version)

        # witch-main
        test.run("tests/ui/cache-pages/witch-main.py", flet_version, ui=True)

        # without-main
        test.run("tests/ui/cache-pages/without-main.py", flet_version, ui=True)

        # flet-app
        if session.python != "3.9":
            test.run("tests/ui/flet-app/src/main.py", flet_version, ui=True)

        # render-page-decorator
        if flet_version in FLET_VERSIONS_NEW:
            test.run("tests/UI/render-page-decorator.py", flet_version, ui=True)

    test.finish(all=True)
