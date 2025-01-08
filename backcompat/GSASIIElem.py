from warnings import warn

from GSASII.GSASIIElem import *

warn(
    "Importing GSASIIElem as a top level module is deprecated, please import "
    + "it as a sub-module of GSASII",
    stacklevel=2,
)
