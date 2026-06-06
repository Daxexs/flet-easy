from typing import Any, Optional

from flet import FontWeight, ScrollMode, Text, View


def page_error_fs(route: str, error_msg: Optional[str] = None) -> View:
    """Standard error view for Flet-Easy rendering failures."""
    controls: list[Any] = [
        Text(
            f"Error in Page '{route}'",
            size=25,
            weight=FontWeight.BOLD,
            color="red",
        )
    ]
    if error_msg:
        controls.append(Text(error_msg, font_family="monospace", color="red"))
    else:
        controls.append(
            Text("An internal error occurred. Check the terminal for more details.", color="red")
        )

    return View(
        route=route,
        controls=controls,
        scroll=ScrollMode.AUTO,
    )
