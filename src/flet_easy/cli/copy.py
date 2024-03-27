from os import listdir, mkdir, path
from pathlib import Path
from shutil import copy, copytree, ignore_patterns

from rich import print


def _copy_template(from_path: str, to_path: str, manifest: bool):
    struct = Path(__file__).parent / from_path
    try:
        mkdir(to_path)

        patterns_to_ignore = [
            "__pycache__",
            "index.html",
            "manifest.json",
            "icons",
            "favicon.png",
        ]

        if manifest == "y":
            patterns_to_ignore = patterns_to_ignore[:1]

        for item in struct.iterdir():
            try:
                if item.is_file():
                    copy(item, to_path)
                elif item.is_dir():
                    copytree(
                        item,
                        to_path / item.name,
                        ignore=ignore_patterns(*patterns_to_ignore),
                    )
            except Exception as e:
                print(e)

        colors = [
            "orange_red1",
            "dark_cyan",
            "gold1",
            "bright_yellow",
            "dodger_blue1",
            "dark_khaki",
            "deep_pink2",
            "light_sea_green",
            "salmon1",
        ]
        n_color = 0

        files_folder = [f for f in listdir(struct)]

        print("\n[spring_green4 bold]> Initializing project: [/spring_green4 bold]")
        for f in files_folder:
            if path.isdir(struct / f) and f != "__pycache__":
                print(f"[{colors[n_color]}] + {f} [/{colors[n_color]}] created")
                n_color += 1

            if path.isfile(struct / f):
                print(f"[{colors[n_color]}] : {f} [/{colors[n_color]}] created")
                n_color += 1

        print("[light_sky_blue3] : pyproject.toml [/light_sky_blue3] created")

        if manifest == "y":
            print("\n[blue]● It has ended correctly. Remember to customize manifest.json and the icons in the assets folder :)[/blue]")
        else:
            print("\n[blue]● It has finished correctly.[/blue]")

    except FileExistsError:
        print(f"\n[red1 bold]Alert:[/red1 bold] A folder with the same name already exists. [green]({to_path})[/green]")
