#!/usr/bin/env python3
# Copyright (c) 2019 The Potahcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test descriptor wallet function."""

from test_framework.test_framework import PotahcoinTestFramework
from test_framework.util import (
    assert_equal,
    assert_raises_rpc_error
)


class WalletDescriptorTest(PotahcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 1
        self.extra_args = [['-keypool=100']]
        self.wallet_names = []

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()
        self.skip_if_no_sqlite()

    def run_test(self):
        # Make a legacy wallet and check it is BDB
        self.nodes[0].createwallet(wallet_name="legacy1", descriptors=False)
        wallet_info = self.nodes[0].getwalletinfo()
        assert_equal(wallet_info['format'], 'bdb')
        self.nodes[0].unloadwallet("legacy1")

        # Make a descriptor wallet
        self.log.info("Making a descriptor wallet")
        self.nodes[0].createwallet(wallet_name="desc1", descriptors=True)

        # A descriptor wallet should have 100 addresses * 3 types = 300 keys
        self.log.info("Checking wallet info")
        wallet_info = self.nodes[0].getwalletinfo()
        assert_equal(wallet_info['format'], 'sqlite')
        assert_equal(wallet_info['keypoolsize'], 300)
        assert_equal(wallet_info['keypoolsize_hd_internal'], 300)
        assert 'keypoololdest' not in wallet_info

        # Check that getnewaddress works
        self.log.info("Test that getnewaddress and getrawchangeaddress work")
        addr = self.nodes[0].getnewaddress("", "legacy")
        addr_info = self.nodes[0].getaddressinfo(addr)
        assert addr_info['desc'].startswith('pkh(')
        assert_equal(addr_info['hdkeypath'], 'm/44\'/1\'/0\'/0/0')

        addr = self.nodes[0].getnewaddress("", "p2sh-segwit")
        addr_info = self.nodes[0].getaddressinfo(addr)
        assert addr_info['desc'].startswith('sh(wpkh(')
        assert_equal(addr_info['hdkeypath'], 'm/49\'/1\'/0\'/0/0')

        addr = self.nodes[0].getnewaddress("", "bech32")
        addr_info = self.nodes[0].getaddressinfo(addr)
        assert addr_info['desc'].startswith('wpkh(')
        assert_equal(addr_info['hdkeypath'], 'm/84\'/1\'/0\'/0/0')

        # Check that getrawchangeaddress works
        addr = self.nodes[0].getrawchangeaddress("legacy")
        addr_info = self.nodes[0].getaddressinfo(addr)
        assert addr_info['desc'].startswith('pkh(')
        assert_equal(addr_info['hdkeypath'], 'm/44\'/1\'/0\'/1/0')

        addr = self.nodes[0].getrawchangeaddress("p2sh-segwit")
        addr_info = self.nodes[0].getaddressinfo(addr)
        assert addr_info['desc'].startswith('sh(wpkh(')
        assert_equal(addr_info['hdkeypath'], 'm/49\'/1\'/0\'/1/0')

        addr = self.nodes[0].getrawchangeaddress("bech32")
        addr_info = self.nodes[0].getaddressinfo(addr)
        assert addr_info['desc'].startswith('wpkh(')
        assert_equal(addr_info['hdkeypath'], 'm/84\'/1\'/0\'/1/0')

        # Make a wallet to receive coins at
        self.nodes[0].createwallet(wallet_name="desc2", descriptors=True)
        recv_wrpc = self.nodes[0].get_wallet_rpc("desc2")
        send_wrpc = self.nodes[0].get_wallet_rpc("desc1")

        # Generate some coins
        send_wrpc.generatetoaddress(101, send_wrpc.getnewaddress())

        # Make transactions
        self.log.info("Test sending and receiving")
        addr = recv_wrpc.getnewaddress()
        send_wrpc.sendtoaddress(addr, 10)

        # Make sure things are disabled
        self.log.info("Test disabled RPCs")
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.importprivkey, "cVpF924EspNh8KjYsfhgY96mmxvT6DgdWiTYMtMjuM74hJaU5psW")
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.importpubkey, send_wrpc.getaddressinfo(send_wrpc.getnewaddress()))
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.importaddress, recv_wrpc.getnewaddress())
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.importmulti, [])
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.addmultisigaddress, 1, [recv_wrpc.getnewaddress()])
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.dumpprivkey, recv_wrpc.getnewaddress())
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.dumpwallet, 'wallet.dump')
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.importwallet, 'wallet.dump')
        assert_raises_rpc_error(-4, "This type of wallet does not support this command", recv_wrpc.rpc.sethdseed)

        self.log.info("Test encryption")
        # Get the master fingerprint before encrypt
        info1 = send_wrpc.getaddressinfo(send_wrpc.getnewaddress())

        # Encrypt wallet 0
        send_wrpc.encryptwallet('pass')
        send_wrpc.walletpassphrase('pass', 10)
        addr = send_wrpc.getnewaddress()
        info2 = send_wrpc.getaddressinfo(addr)
        assert info1['hdmasterfingerprint'] != info2['hdmasterfingerprint']
        send_wrpc.walletlock()
        assert 'hdmasterfingerprint' in send_wrpc.getaddressinfo(send_wrpc.getnewaddress())
        info3 = send_wrpc.getaddressinfo(addr)
        assert_equal(info2['desc'], info3['desc'])

        self.log.info("Test that getnewaddress still works after keypool is exhausted in an encrypted wallet")
        for _ in range(500):
            send_wrpc.getnewaddress()

        self.log.info("Test that unlock is needed when deriving only hardened keys in an encrypted wallet")
        send_wrpc.walletpassphrase('pass', 10)
        send_wrpc.importdescriptors([{
            "desc": "wpkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/0h/*h)#y4dfsj7n",
            "timestamp": "now",
            "range": [0,10],
            "active": True
        }])
        send_wrpc.walletlock()
        # Exhaust keypool of 100
        for _ in range(100):
            send_wrpc.getnewaddress(address_type='bech32')
        # This should now error
        assert_raises_rpc_error(-12, "Keypool ran out, please call keypoolrefill first", send_wrpc.getnewaddress, '', 'bech32')

        self.log.info("Test born encrypted wallets")
        self.nodes[0].createwallet('desc_enc', False, False, 'pass', False, True)
        enc_rpc = self.nodes[0].get_wallet_rpc('desc_enc')
        enc_rpc.getnewaddress() # Makes sure that we can get a new address from a born encrypted wallet

        self.log.info("Test blank descriptor wallets")
        self.nodes[0].createwallet(wallet_name='desc_blank', blank=True, descriptors=True)
        blank_rpc = self.nodes[0].get_wallet_rpc('desc_blank')
        assert_raises_rpc_error(-4, 'This wallet has no available keys', blank_rpc.getnewaddress)

        self.log.info("Test descriptor wallet with disabled private keys")
        self.nodes[0].createwallet(wallet_name='desc_no_priv', disable_private_keys=True, descriptors=True)
        nopriv_rpc = self.nodes[0].get_wallet_rpc('desc_no_priv')
        assert_raises_rpc_error(-4, 'This wallet has no available keys', nopriv_rpc.getnewaddress)

if __name__ == '__main__':
    WalletDescriptorTest().main ()
