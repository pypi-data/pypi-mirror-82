# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "pyc_wheel"
__summary__      = "Compile all py files in a wheel to pyc files."
__uri__          = "https://pypi.org/project/pyc_wheel/"
__version_info__ = type("version_info", (), dict(major=1, minor=2, micro=3,
                        releaselevel="final", serial=0))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(alpha="a", beta="b", candidate="rc", final="",
                        post=".post", dev=".dev")[__version_info__.releaselevel],
                   __version_info__.serial
                   if __version_info__.releaselevel != "final" else "")
__author__       = "Grant Patten, Adam Karpierz"
__maintainer__   = "Adam Karpierz"
__email__        = "adam@karpierz.net"
__copyright__    = "Copyright (c) 2019-2020 {0}".format(__author__)
__license__      = "MIT License ; {0}".format(
                   "https://opensource.org/licenses/MIT")
