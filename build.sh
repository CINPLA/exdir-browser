#!/bin/bash
which pyrcc5
pyrcc5 -o exdirbrowser/qml_qrc.py exdirbrowser/qml.qrc
python setup.py install
