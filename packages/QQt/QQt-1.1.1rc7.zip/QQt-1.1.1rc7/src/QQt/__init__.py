# Copyright (c) 2012-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

from .__about__  import * ; del __about__  # noqa
from .__config__ import origin

import sys
__import__(origin)

QQt = sys.modules[__name__]

# Utils
from ._utils import StreamEmitter

# Wrapper for origin.

sys.modules[__name__] = sys.modules[origin]
for name, module in sys.modules.copy().items():
    if name.startswith(origin + "."):
        sys.modules[__name__ + name[len(origin):]] = sys.modules[name]

# Monkey-patch for vtk.qt (vtk==8.1.2) for PySide2 as backend.

try:
    import vtk
    from vtk.qt import PyQtImpl
except ImportError:
    PyQtImpl = None
else:
    if PyQtImpl is None:
        PyQtImpl = "PySide2"
        if (PyQtImpl in sys.modules and
            (vtk.VTK_MAJOR_VERSION, vtk.VTK_MINOR_VERSION) == (8, 1)):
            sys.modules["vtk.qt"].PyQtImpl = PyQtImpl
            sys.modules[__name__] = QQt
            from .vtk.qt import QVTKRenderWindowInteractor as patched
            sys.modules[__name__] = sys.modules[origin]
            sys.modules["vtk.qt.QVTKRenderWindowInteractor"] = patched

sys.modules[origin].StreamEmitter = StreamEmitter
