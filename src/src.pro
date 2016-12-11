TEMPLATE = app

QT += qml quick widgets gui
CONFIG += c++14

CONFIG += c++11
LIBS += -lboost_system -lboost_filesystem -lyaml-cpp

RESOURCES += qml.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    models/exdirattributesmodel.h \
    models/exdirmodel.h \
    models/exdirtreemodel.h \
    views/matrixview.h \
    elegant-exdir/object.h \
    elegant-exdir/attribute.h \
    elegant-exdir/dataset_p.h \
    elegant-exdir/dataset.h \
    elegant-exdir/file.h \
    elegant-exdir/group.h \
    elegant-exdir/converters/armadillo-converters.h \
    elegant-exdir/converters/native-converters.h \
    elegant-exdir/converters/std-converters.h \
    elegant-exdir/io/reader.h \
    elegant-exdir/io/typehelper.h \
    elegant-exdir/io/writer.h \
    elegant-exdir/utils/demangle.h \
    elegant-exdir/utils/errorhelper.h \
    elegant-exdir/utils/logging.h \
    elegant-exdir/datatype.h

SOURCES += \
    main.cpp \
    models/exdirattributesmodel.cpp \
    models/exdirmodel.cpp \
    models/exdirtreemodel.cpp \
    views/matrixview.cpp \
    elegant-exdir/object.cpp \
    elegant-exdir/attribute.cpp \
    elegant-exdir/attribute.tpp \
    elegant-exdir/dataset.cpp \
    elegant-exdir/dataset.tpp \
    elegant-exdir/errorhelper.cpp \
    elegant-exdir/file.cpp \
    elegant-exdir/group.cpp \
    elegant-exdir/object.tpp \
    elegant-exdir/datatype.cpp

CONFIG += conan_basic_setup
include(../vendor/elegant-npy/package.pri)
