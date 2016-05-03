"""GSMT Tools module."""
import errno
import os


def mkdir_p(path):
    """Create folder if not exists."""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def remove_newline(string):
    """If newline character on end remove it."""
    if string[-1] == "\n":
        return string[:-1]
    return string
