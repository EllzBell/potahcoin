// Copyright (c) 2017-2019 The Potahcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef POTAHCOIN_CONSENSUS_TX_CHECK_H
#define POTAHCOIN_CONSENSUS_TX_CHECK_H

/**
 * Context-independent transaction checking code that can be called outside the
 * potahcoin server and doesn't depend on chain or mempool state. Transaction
 * verification code that does call server functions or depend on server state
 * belongs in tx_verify.h/cpp instead.
 */

class CTransaction;
class TxValidationState;

bool CheckTransaction(const CTransaction& tx, TxValidationState& state);

#endif // POTAHCOIN_CONSENSUS_TX_CHECK_H
