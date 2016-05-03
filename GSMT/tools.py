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
