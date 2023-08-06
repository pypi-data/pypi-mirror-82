"""Tools for handling I/O.

This module provides common functions when working with I/O.
"""

from pathlib import Path
from typing import List, Tuple, Union

from mlxtk.util import make_path

HDF5_MAGIC_NUMBER = bytes([0x89, 0x48, 0x44, 0x46, 0x0D, 0x0A, 0x1A, 0x0A])
"""bytes: Magic number of the HDF5 file format.
"""


def is_hdf5_path(path: Union[str, Path]) -> Tuple[bool, Path, str]:
    """Parse a path which potentially resides inside a HDF5 file

    This function checks wether path points to a regular file on the disk. If
    this is ``False``, the full path and an empty string are returned.
    If path is a path to a HDF5 file any trailing components are considered to
    denote the interior path inside the HDF5 file. In this case ``True``, the
    path to the HDF5 file and the interior path are returned.

    Args:
        path (str): path to a file

    Returns:
        Tuple[bool, str, str]: whether this path is a path in a HDF5 file, path
            to the file and interior path.
    """
    path = make_path(path).resolve()
    built_path = Path(path.parts[0])

    for part in path.parts[1:]:
        built_path /= part

        if is_hdf5_file(built_path):
            return True, built_path, str(path.relative_to(built_path))

    return False, path, ""


def is_hdf5_file(path: Path) -> bool:
    """Check if a file is a HDF5 file using the magic number

    Args:
        path (str): path to the file

    Returns:
        bool: Whether path points to a HDF5 file.
    """
    if not path.exists():
        return False

    if not path.is_file():
        return False

    with open(path, "rb") as fptr:
        return fptr.read(8) == HDF5_MAGIC_NUMBER
