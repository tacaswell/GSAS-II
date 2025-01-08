from warnings import warn

from GSASII.GSASIIstrIO import *

warn(
    "Importing GSASIIstrIO as a top level module is deprecated, please import "
    + "it as a sub-module of GSASII",
    stacklevel=2,
)