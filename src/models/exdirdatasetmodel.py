from PyQt5.QtCore import *
from PyQt5.QtQml import *
import exdir

class ExdirDatasetModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._currentSlice = 0
        self._sliceCount = 0
        self._source = QUrl()
        self.hasData = False
        self._hasUnsavedChanges = False
        self._dataset = ""
        self.dataPointer = None
    
    def rowCount(self, parent=QModelIndex()):
        if not self.hasData:
            return 0

        if len(self.dataPointer.shape) > 0:
            return self.dataPointer.shape[0]
        else:
            return 0

    def columnCount(self, parent=QModelIndex()):
        if not self.hasData:
            return 0

        if len(self.dataPointer.shape) > 1:
            return self.dataPointer.shape[1]
        else:
            return 1

    def inBounds(self, index):        
        if not self.hasData:
            return False

        shape = self.dataPointer.shape
        if len(shape) > 0:
            if index.row() < 0 or index.row() >= shape[0]:
                return False
        if len(shape) > 1:
            if index.column() < 0 or index.column() >= shape[1]:
                return False
        return True

    def hasUnsavedChanges(self):
        return self._hasUnsavedChanges

    def currentSlice(self):
        return self._currentSlice

    def sliceCount(self):
        return self._sliceCount

    def data(self, index, role):
        if not self.hasData:
            return QVariant()

        if role == Qt.DisplayRole:
            if self.inBounds(index):
                if len(self.dataPointer.shape) > 2:
                    return self.dataPointer[index.row(), index.column(), self._currentSlice]
                elif len(self.dataPointer.shape) > 1:
                    return self.dataPointer[index.row(), index.column()]
                elif len(self.dataPointer.shape) > 0:
                    return self.dataPointer[index.row()]
                else: 
                    return QVariant()
            else:
                print("Requested index out of bounds", index.row(), index.column())
            return QVariant(0.0)
        else:
            return QVariant()

    def setData(self, index, value, role):
        if not index.isValid():        
            return False

        if not self.inBounds((index)):        
            return False

        # if not value.canConvert<double>():        
            # TODO canconvert?
            # return False

        # TODO set data
        self._hasUnsavedChanges = True
        self.dataChanged.emit(index, index)
        self.hasUnsavedChangesChanged.emit(self._hasUnsavedChanges)
        return True

    def roleNames(self):
        return {
            Qt.DisplayRole: "value"
        }

    def dataset(self):
        return self._dataset

    def source(self):
        return self._source

    def setDataset(self, dataSet):
        if self._dataset == dataSet:
            return

        self._dataset = dataSet
        self.load()
        self.datasetChanged.emit(dataSet)

    def setSource(self, source):
        print("Setting source to", source)
        if self._source == source:
            return

        self._source = source
        self.load()
        self.sourceChanged.emit(source)

    def setCurrentSlice(self, currentSlice):
        if self._currentSlice == currentSlice:
            return

        self._currentSlice = currentSlice
        self.dataChanged.emit(index(0, 0), index(rowCount() - 1, columnCount() - 1))
        self.currentSliceChanged.emit(currentSlice)

    def setSliceCount(self, sliceCount):
        if self._sliceCount == sliceCount:
            return

        self._sliceCount = sliceCount
        self.sliceCountChanged.emit(sliceCount)

    def load(self):
        self.hasData = False
        self.dimensionCount = 0

        if not self._source.isValid() or self._dataset == "":
            self.dataChanged.emit(QModelIndex(), QModelIndex())
            return

        fileNameString = self.source.toLocalFile()
        datasetName = self._dataset
        file = exdir.File(fileNameString)
        
        print("Dataset name", datasetName)
        
        dataset = file[datasetName]
        if isinstance(dataset, exdir.core.Dataset):
            print("Is dataset!")
            self.hasData = True
            # TODO can we request shape without loading all the data?
            # data = dataset.data
            # self.dataPointer = dataset
            self.dataPointer = dataset.data # TODO point to dataset when we don't reload file every time
            # self.currentType = dataset.datatype()
            # self.dimensionCount = dataset.dimensionCount()
            # extents = dataset.extents()
            
            shape = dataset.shape
            self.dimensionCount = len(shape)
            
            print("Dimension count", self.dimensionCount)
            
            if self.dimensionCount == 3:
                self.setSliceCount(extents[0])


            # TODO implement
            # switch(self.currentType)        
            # case Datatype.Type.Int:
            #     self.dataPointer = dataset.value<arma.Cube<int>>(Object.ConversionFlags.GreaterThanOrEqualDimensionCount)
            #     break
            # case Datatype.Type.Long:
            #     self.dataPointer = dataset.value<arma.Cube<long int>>(Object.ConversionFlags.GreaterThanOrEqualDimensionCount)
            #     break
            # case Datatype.Type.Float:
            #     self.dataPointer = dataset.value<arma.Cube<float>>(Object.ConversionFlags.GreaterThanOrEqualDimensionCount)
            #     break
            # case Datatype.Type.Double:
            #     self.dataPointer = dataset.value<arma.Cube<double>>(Object.ConversionFlags.GreaterThanOrEqualDimensionCount)
            #     break
            # default:
            #     qWarning() << "Could not read self type of data"
            #     self.hasData = False
            #     self.dimensionCount = 0
            #     break
            # 
            # if self.dimensionCount == 1:            # transpose to visualize 1D as column instead of row
            #     boost.apply_visitor(transpose_visitor(), self.dataPointer)


        if not self.hasData or self.dimensionCount != 3:
            self.setSliceCount(1)

        self._hasUnsavedChanges = False
        self.sliceCountChanged.emit(self._sliceCount)
        self.dataChanged.emit(QModelIndex(), QModelIndex())
        self.hasUnsavedChangesChanged.emit(self._hasUnsavedChanges)

    def save(self):
        pass
        # TODO implement save
        # # TODO keep working on the same file when loading/saving
        # 
        # qDebug() << "Saving file"
        # if not self.source.isValid() or self._dataset.isEmpty():        return False
        # 
        # fileNameString = QQmlFile.urlToLocalFileOrQrc(self.source)
        # datasetName = self._dataset.toStdString()
        # qDebug() << "Loading" << self.dataset << "in" << fileNameString
        # File file(fileNameString.toStdString(), File.OpenMode.ReadWrite)
        # 
        # if file[datasetName].isDataset():        dataset = file[datasetName]
        #     boost.apply_visitor(save_visitor(dataset, self.dimensionCount), self.dataPointer)
        # 
        # self.hasUnsavedChanges = False
        # hasUnsavedChangesChanged.emit(self.hasUnsavedChanges)
        # return True
        
    datasetChanged = pyqtSignal(str)
    sourceChanged = pyqtSignal(QUrl)
    hasUnsavedChangesChanged = pyqtSignal(bool)
    currentSliceChanged = pyqtSignal(int)
    sliceCountChanged = pyqtSignal(int)

    source = pyqtProperty(QUrl, source, setSource, notify=sourceChanged)
    dataset = pyqtProperty(str, dataset, setDataset, notify=datasetChanged)
    currentSlice = pyqtProperty(int, currentSlice, setCurrentSlice, notify=currentSliceChanged)
    hasUnsavedChanges = pyqtProperty(bool, hasUnsavedChanges, notify=hasUnsavedChangesChanged)
    sliceCount = pyqtProperty(int, sliceCount, notify=sliceCountChanged)
