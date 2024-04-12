from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers
from os import listdir, path
from typing import List

from flet_easy.pagesy import AddPagesy


def automatic_routing(dir: str) -> List[AddPagesy]:
    """
    A function that automatically routes through a directory to find Python files, extract AddPagesy objects, and return a list of them.

    Parameters:
    - dir (str): The directory path to search for Python files.

    Returns:
    - List[AddPagesy]: A list of AddPagesy objects found in the specified directory.
    """

    pages = []
    for file in listdir(dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            module_route = path.join(dir, file)
            spec = spec_from_file_location(module_name, module_route)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            for _, object_page in getmembers(module):
                if isinstance(object_page, AddPagesy):
                    pages.append(object_page)
    if len(pages) == 0:
        raise ValueError(
            "No instances of AddPagesy found. Check the assigned path of the 'path_view' parameter of the class (FletEasy)."
        )

    return pages
