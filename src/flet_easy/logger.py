import logging

try:
    from rich.logging import RichHandler

    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False


class ColorFormatter(logging.Formatter):
    def format(self, record):
        record.name = f"[bold]{record.name}[/]:"
        return super().format(record)


class OnlyMyLogsFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith("flet_easy")


class LoggingFletEasy:
    """Logger for Flet Easy"""

    _logger_activado = False

    @classmethod
    def enable(cls, level: int = logging.INFO) -> None:
        """
        Enables the logging system only ONCE.
        - With rich: uses its own format.
        - Without rich: forces the exact format of the image.
        """
        if cls._logger_activado:
            return

        root = logging.getLogger()
        root.setLevel(level)

        if _RICH_AVAILABLE:
            fmt = ColorFormatter(fmt="%(name)s %(message)s")
            console = RichHandler(
                level=level,
                show_level=True,
                rich_tracebacks=True,
                show_time=True,
                omit_repeated_times=False,
                show_path=True,
                markup=True,
                log_time_format="%Y-%m-%d %H:%M:%S",
            )
            console.setFormatter(fmt)

        else:
            fmt = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s | %(pathname)s : %(lineno)d",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console = logging.StreamHandler()

            console.setFormatter(fmt)

        console.addFilter(OnlyMyLogsFilter())
        root.addHandler(console)
        cls._logger_activado = True


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the given name.
    Example: logger = get_logger("Init")
    """
    full_name = name if name.startswith("flet_easy") else f"flet_easy.{name}"
    return logging.getLogger(full_name)
