import argparse
import contextlib

from flet_easy.exceptions import FletEasyError

try:
    from cookiecutter.main import cookiecutter
    from rich_argparse import RichHelpFormatter
except ImportError:
    raise FletEasyError('To use the cli (fs) Install: "pip install flet-easy[all] --upgrade"')

VERSION = "0.2.9"

RichHelpFormatter.styles["argparse.text"] = "italic"
RichHelpFormatter.styles["argparse.help"] = "light_sky_blue3"
RichHelpFormatter.styles["argparse.prog"] = "blue"


def init_app():
    cookiecutter(
        template="gh:Daxexs/fs-template-dxs",
        overwrite_if_exists=True,
        checkout="main",
        accept_hooks=True,
    )


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
