#ifndef MATRIXVIEW_H
#define MATRIXVIEW_H

#include <QElapsedTimer>
#include <QQuickItem>
#include <QVariant>
#include <QModelIndex>
#include <QTimer>

class QQmlComponent
class QAbstractTableModel

struct CachedItem
    CachedItem() {
    CachedItem(QQuickItem *item_, int row_, int column_)
        : item(item_)
        , row(row_)
        , column(column_)

    QQuickItem *item = nullptr
    long row = -1
    long column = -1
    dummy = True


class MatrixView : public QQuickItem
    Q_OBJECT
    Q_PROPERTY(QVariant model READ model WRITE setModel NOTIFY modelChanged)
    Q_PROPERTY(QQmlComponent *delegate READ delegate WRITE setDelegate NOTIFY delegateChanged)
    Q_PROPERTY(double cellWidth READ cellWidth WRITE setCellWidth NOTIFY cellWidthChanged)
    Q_PROPERTY(double cellHeight READ cellHeight WRITE setCellHeight NOTIFY cellHeightChanged)
    Q_PROPERTY(QModelIndex currentIndex READ currentIndex WRITE setCurrentIndex NOTIFY currentIndexChanged)

public:
    MatrixView()

    QVariant model()
    QQmlComponent * delegate()
    double cellWidth()
    double cellHeight()

    QModelIndex currentIndex()

    void focusItemAt(int row, column)
    QRectF viewportRect()
    QRectF itemRect(int row, column)
signals:
    void modelChanged(QVariant model)
    void delegateChanged(QQmlComponent * delegate)
    void cellWidthChanged(double cellWidth)
    void cellHeightChanged(double cellHeight)

    void currentIndexChanged(QModelIndex currentIndex)

public slots:
    void setModel(QVariant model)
    void setDelegate(QQmlComponent * delegate)
    void setCellWidth(double cellWidth)
    void setCellHeight(double cellHeight)
    void updateView()
    void clear()

    void setCurrentIndex(QModelIndex currentIndex)

private slots:
    void reconnectObjects()
    void handleDataChange( QModelIndex &topLeft, &bottomRight, roles = QVector<int>())

    void updateViewFully()
private:
    bool shouldSkip(long int row, int column)
    void updateContextData(int row, column, *context)

    QAbstractTableModel *m_model = nullptr
    QQmlComponent * m_delegate
    QVector<CachedItem> m_cachedItems

    QRectF m_previousViewportRect
    QRectF m_previousViewportRectFully
    QElapsedTimer timer
    m_cellWidth = 100
    m_cellHeight = 30

    QQuickItem *m_flickable = nullptr
    QQuickItem *m_viewport
    QModelIndex m_currentIndex

    QTimer m_updateTimer

    # QQuickItem interface
protected:
    virtual void keyPressEvent(QKeyEvent *event) override


#endif # MATRIXVIEW_H
