from warnings import warn

from GSASII.GSASIIexprGUI import *

warn(
    "Importing GSASIIexprGUI as a top level module is deprecated, please import "
    + "it as a sub-module of GSASII",
    stacklevel=2,
)