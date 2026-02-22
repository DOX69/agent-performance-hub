"""APH — Agent Performance Hub CLI.

Manage AI agent skills across your projects.
Install, update, and organize skills from the agent-performance-hub.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("aph-cli")
except PackageNotFoundError:
    # Package not installed
    try:
        from ._version import version as __version__
    except ImportError:
        __version__ = "0.0.0+unknown"
