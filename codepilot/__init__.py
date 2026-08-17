from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version("codepilot")
except PackageNotFoundError:
    __version__ = "0.2.0"


__all__ = ["__version__"]
