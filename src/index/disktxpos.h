// Copyright (c) 2019 The Potahcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef POTAHCOIN_INDEX_DISKTXPOS_H
#define POTAHCOIN_INDEX_DISKTXPOS_H

#include <flatfile.h>
#include <serialize.h>

struct CDiskTxPos : public FlatFilePos
{
    unsigned int nTxOffset; // after header

    SERIALIZE_METHODS(CDiskTxPos, obj)
    {
        READWRITEAS(FlatFilePos, obj);
        READWRITE(VARINT(obj.nTxOffset));
    }

    CDiskTxPos(const FlatFilePos &blockIn, unsigned int nTxOffsetIn) : FlatFilePos(blockIn.nFile, blockIn.nPos), nTxOffset(nTxOffsetIn) {
    }

    CDiskTxPos() {
        SetNull();
    }

    void SetNull() {
        FlatFilePos::SetNull();
        nTxOffset = 0;
    }
};


#endif // POTAHCOIN_INDEX_DISKTXPOS_H
