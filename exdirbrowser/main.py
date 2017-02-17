#!/usr/bin/env python

import ctypes
from ctypes.util import find_library

# OpenGL fix (must be set before other imports)
libGL = find_library("GL")
ctypes.CDLL(libGL, ctypes.RTLD_GLOBAL)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *

from .models.exdirtreemodel import *
from .models.exdirdatasetmodel import *
from .models.exdirattributesmodel import *
from .views.matrixview import *
from . import qml_qrc
import sys


def main():
    qmlRegisterType(ExdirDatasetModel, "H5Vis", 1, 0, "ExdirDatasetModel")
    qmlRegisterType(ExdirTreeModel, "H5Vis", 1, 0, "ExdirTreeModel")
    qmlRegisterType(ExdirTreeItem, "H5Vis", 1, 0, "ExdirTreeItem")
    qmlRegisterType(ExdirAttributesModel, "H5Vis", 1, 0, "ExdirAttributesModel")
    qmlRegisterType(MatrixView, "H5Vis", 1, 0, "MatrixView")

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load(QUrl("qrc:/qml/main.qml"))

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
