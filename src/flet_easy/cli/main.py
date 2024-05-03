import argparse
import contextlib
from pathlib import Path

from rich.prompt import Prompt
from rich_argparse import RichHelpFormatter
from tomlkit import dump

from .copy import _copy_template

VERSION = "0.2.2"

RichHelpFormatter.styles["argparse.text"] = "italic"
RichHelpFormatter.styles["argparse.help"] = "light_sky_blue3"
RichHelpFormatter.styles["argparse.prog"] = "blue"


def init_app():
    toml_dict = {"project": {}}
    pwd = Path.cwd()

    name = Prompt.ask("Projet Name", default=pwd.name)
    version = Prompt.ask("Project Version", default="0.1.0")
    license = Prompt.ask(
        "Project License",
        default="MIT",
    )
    author = Prompt.ask("Project Author")
    email = Prompt.ask("Email Author")
    manifest = Prompt.ask(
        "Requires creation of manifest.json (Web-PWA)", choices=["n", "y"], default="n"
    )

    toml_dict["project"]["name"] = name
    toml_dict["project"]["version"] = version
    toml_dict["project"]["license"] = license
    toml_dict["project"]["authors"] = [{"name": author, "email": email}]
    toml_dict["project"]["dependencies"] = ["flet", "flet-easy"]

    _copy_template("templates", pwd / name, manifest)

    with open(f"{pwd}/{name}/pyproject.toml", "w") as file:
        dump(toml_dict, file)


def run():
    parser = argparse.ArgumentParser(
        description="CLI for Flet-Easys.", formatter_class=RichHelpFormatter
    )
    parser.add_argument(
        "--version", "-v", action="version", help=" Flet-Easy Version", version=VERSION
    )

    subparsers = parser.add_subparsers(dest="command", title="Comandos")

    #  Subcommand 'init'
    subparsers.add_parser(
        "init",
        aliases=["i"],
        help="Create the structure of the app",
        formatter_class=RichHelpFormatter,
    )

    args = parser.parse_args()

    if args.command == "init" or args.command == "i":
        with contextlib.suppress(KeyboardInterrupt):
            init_app()
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
