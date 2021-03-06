import os
import typer
import webbrowser
import subprocess

from pathlib import Path
from functools import wraps

app = typer.Typer()


def typer_cli(f):
    # @app.command() does not work, dunno why
    @wraps(f)
    def wrapper():
        return typer.run(f)

    return wrapper


def print_styled_command(command):
    typer.echo(
        typer.style(
            "Running command line:",
            fg=typer.colors.WHITE,
            bg=typer.colors.GREEN,
            bold=True,
        )
    )
    typer.echo(typer.style(" ".join(command), bold=True) + "\n")


def run_command(command, debug=False, cwd=None, env=None):
    command = command.split()
    if debug:
        print_styled_command(command)
    subprocess.run(command, cwd=cwd, env=env)


@typer_cli
def test(test_path: str = typer.Argument(None)):
    command = "python runtests.py"
    if test_path is None:
        test_path = "tests"
    command = f"{command} {test_path}"
    run_command(command, debug=True)


@typer_cli
def pytest(test_path: str = typer.Argument(None)):
    command = "pytest"
    if test_path is not None:
        command = f"{command} {test_path}"
    run_command(command, debug=True)


@typer_cli
def flake8():
    command = "flake8 ."
    run_command(command, debug=True)


@typer_cli
def black():
    command = "black ."
    run_command(command, debug=True)


@typer_cli
def coverage():
    commands = [
        "coverage run --source cast --branch runtests.py tests",
        "coverage report -m",
        "coverage html",
    ]
    for command in commands:
        run_command(command, debug=True)
    file_url = "file://" + str(Path("htmlcov/index.html").resolve())
    webbrowser.open_new_tab(file_url)


@typer_cli
def clean_build():
    commands = [
        "rm -fr build/",
        "rm -fr dist/",
        "rm -fr *.egg-info",
        "rm -fr __pycache__",
    ]
    for command in commands:
        run_command(command, debug=True)


@typer_cli
def clean_pyc():
    commands = [
        "find . -name '*.pyc' -exec rm -f {} +",
        "find . -name '*.pyo' -exec rm -f {} +",
        "find . -name '*~' -exec rm -f {} +",
    ]
    for command in commands:
        run_command(command, debug=True)


@typer_cli
def clean():
    clean_build()
    clean_pyc()


@typer_cli
def notebook():
    env = os.environ.copy()
    env["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    command = (
        "python ../manage.py shell_plus --notebook"
    )
    run_command(command, cwd="notebooks", debug=True, env=env)
