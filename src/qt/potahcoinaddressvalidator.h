// Copyright (c) 2011-2014 The Potahcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef POTAHCOIN_QT_POTAHCOINADDRESSVALIDATOR_H
#define POTAHCOIN_QT_POTAHCOINADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class PotahcoinAddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit PotahcoinAddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const override;
};

/** Potahcoin address widget validator, checks for a valid potahcoin address.
 */
class PotahcoinAddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit PotahcoinAddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const override;
};

#endif // POTAHCOIN_QT_POTAHCOINADDRESSVALIDATOR_H
