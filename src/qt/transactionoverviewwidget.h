// Copyright (c) 2021 The Potahcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef POTAHCOIN_QT_TRANSACTIONOVERVIEWWIDGET_H
#define POTAHCOIN_QT_TRANSACTIONOVERVIEWWIDGET_H

#include <qt/transactiontablemodel.h>

#include <QListView>
#include <QSize>
#include <QSizePolicy>

QT_BEGIN_NAMESPACE
class QShowEvent;
class QWidget;
QT_END_NAMESPACE

class TransactionOverviewWidget : public QListView
{
    Q_OBJECT

public:
    explicit TransactionOverviewWidget(QWidget* parent = nullptr) : QListView(parent) {}

    QSize sizeHint() const override
    {
        return {sizeHintForColumn(TransactionTableModel::ToAddress), QListView::sizeHint().height()};
    }

protected:
    void showEvent(QShowEvent* event) override
    {
        Q_UNUSED(event);
        QSizePolicy sp = sizePolicy();
        sp.setHorizontalPolicy(QSizePolicy::Preferred);
        setSizePolicy(sp);
    }
};

#endif // POTAHCOIN_QT_TRANSACTIONOVERVIEWWIDGET_H
