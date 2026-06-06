from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers
from os import scandir
from pathlib import Path
from sys import modules
from typing import Optional, Union

from flet_easy.core.pages import AddPagesy
from flet_easy.exceptions import ConfigurationError
from flet_easy.logger import get_logger


def automatic_routing(dir_path: Union[Path, str]) -> Optional[list[AddPagesy]]:
    """
    A function that automatically routes through a directory to find Python files,
    extract AddPagesy objects, and return a list of them.

    Parameters:
    - dir_path (str): The directory path to search for Python files.

    Returns:
    - List[AddPagesy]: A list of AddPagesy objects found in the specified directory.
    """
    if not dir_path:
        return None

    pages: list[AddPagesy] = []
    logger = get_logger("Automatic routing")

    try:
        entries = list(scandir(dir_path))
    except OSError as e:
        logger.error(f"Error listing directory {dir_path}: {e}")
        raise ConfigurationError(
            "No instances of AddPagesy found. Check the assigned path of the 'path_views' parameter of the class (FletEasy)."
        )

    # Deduplicate in case both .py and .pyc exist (e.g. during dev with __pycache__ mixed)
    processed_modules: set[str] = set()

    for entry in entries:
        # Process .py and .pyc files, skip __init__ files and non-Python files
        if not entry.is_file() or not (entry.name.endswith(".py") or entry.name.endswith(".pyc")):
            continue

        if entry.name.startswith("__init__."):
            continue

        file_path = entry.path
        stem = Path(entry.name).stem
        if stem in processed_modules:
            continue
        processed_modules.add(stem)

        module_name = f"flet_easy_auto_{stem}"

        try:
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
                        logger.debug("Adding AddPagesy automatic routing: %s", obj)
        except Exception as e:
            logger.error(f"Error processing file {entry.name}: {e}")
            continue

    if not pages:
        raise ConfigurationError(
            "No instances of AddPagesy found. Check the assigned path of the 'path_views' parameter of the class (FletEasy)."
        )

    logger.info("Automatic routing completed successfully: %d Pagesy objects", len(pages))
    return pages
