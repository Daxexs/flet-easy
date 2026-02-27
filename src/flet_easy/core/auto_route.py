from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers
from os import listdir, path
from sys import modules
from typing import List, Optional

from flet_easy.core.pages import AddPagesy
from flet_easy.exceptions import ConfigurationError
from flet_easy.logger import get_logger


def automatic_routing(dir: str) -> Optional[List[AddPagesy]]:
    """
    A function that automatically routes through a directory to find Python files,
    extract AddPagesy objects, and return a list of them.

    Parameters:
    - dir (str): The directory path to search for Python files.

    Returns:
    - List[AddPagesy]: A list of AddPagesy objects found in the specified directory.
    """
    if not dir:
        return None

    pages = []
    logger = get_logger("Automatic routing")

    python_files = [
        file
        for file in listdir(dir)
        if (file.endswith(".py") or file.endswith(".pyc")) and file != "__init__.py"
    ]

    for file in python_files:
        file_path = path.join(dir, file)
        module_name = f"flet_easy_auto_{path.splitext(file)[0]}"

        try:
            if not isinstance(file_path, str):
                file_path = str(file_path)

            spec = spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                continue

            module = module_from_spec(spec)

            if hasattr(module, "__dict__"):
                modules[module_name] = module
                spec.loader.exec_module(module)

                for _, obj in getmembers(module):
                    if isinstance(obj, AddPagesy):
                        pages.append(obj)
                        logger.debug(f"Adding AddPagesy automatic routing: {obj}")
        except Exception as e:
            logger.error(f"Error processing file {file}: {e}")
            continue

    if not pages:
        raise ConfigurationError(
            "No instances of AddPagesy found. Check the assigned path of the 'path_views' parameter of the class (FletEasy)."
        )

    logger.info(f"Automatic routing completed successfully: {len(pages)} Pagesy objects")
    return pages
