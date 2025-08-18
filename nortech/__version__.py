try:
    from importlib.metadata import version

    __version__ = version("nortech")
except Exception:
    __version__ = "unknown"
