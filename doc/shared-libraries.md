Shared Libraries
================

## potahcoinconsensus

The purpose of this library is to make the verification functionality that is critical to Potahcoin's consensus available to other applications, e.g. to language bindings.

### API

The interface is defined in the C header `potahcoinconsensus.h` located in `src/script/potahcoinconsensus.h`.

#### Version

`potahcoinconsensus_version` returns an `unsigned int` with the API version *(currently `1`)*.

#### Script Validation

`potahcoinconsensus_verify_script` returns an `int` with the status of the verification. It will be `1` if the input script correctly spends the previous output `scriptPubKey`.

##### Parameters
- `const unsigned char *scriptPubKey` - The previous output script that encumbers spending.
- `unsigned int scriptPubKeyLen` - The number of bytes for the `scriptPubKey`.
- `const unsigned char *txTo` - The transaction with the input that is spending the previous output.
- `unsigned int txToLen` - The number of bytes for the `txTo`.
- `unsigned int nIn` - The index of the input in `txTo` that spends the `scriptPubKey`.
- `unsigned int flags` - The script validation flags *(see below)*.
- `potahcoinconsensus_error* err` - Will have the error/success code for the operation *(see below)*.

##### Script Flags
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_NONE`
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_P2SH` - Evaluate P2SH ([BIP16](https://github.com/potahcoin/bips/blob/master/bip-0016.mediawiki)) subscripts
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_DERSIG` - Enforce strict DER ([BIP66](https://github.com/potahcoin/bips/blob/master/bip-0066.mediawiki)) compliance
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_NULLDUMMY` - Enforce NULLDUMMY ([BIP147](https://github.com/potahcoin/bips/blob/master/bip-0147.mediawiki))
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_CHECKLOCKTIMEVERIFY` - Enable CHECKLOCKTIMEVERIFY ([BIP65](https://github.com/potahcoin/bips/blob/master/bip-0065.mediawiki))
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_CHECKSEQUENCEVERIFY` - Enable CHECKSEQUENCEVERIFY ([BIP112](https://github.com/potahcoin/bips/blob/master/bip-0112.mediawiki))
- `potahcoinconsensus_SCRIPT_FLAGS_VERIFY_WITNESS` - Enable WITNESS ([BIP141](https://github.com/potahcoin/bips/blob/master/bip-0141.mediawiki))

##### Errors
- `potahcoinconsensus_ERR_OK` - No errors with input parameters *(see the return value of `potahcoinconsensus_verify_script` for the verification status)*
- `potahcoinconsensus_ERR_TX_INDEX` - An invalid index for `txTo`
- `potahcoinconsensus_ERR_TX_SIZE_MISMATCH` - `txToLen` did not match with the size of `txTo`
- `potahcoinconsensus_ERR_DESERIALIZE` - An error deserializing `txTo`
- `potahcoinconsensus_ERR_AMOUNT_REQUIRED` - Input amount is required if WITNESS is used

### Example Implementations
- [NPotahcoin](https://github.com/NicolasDorier/NPotahcoin/blob/master/NPotahcoin/Script.cs#L814) (.NET Bindings)
- [node-libpotahcoinconsensus](https://github.com/bitpay/node-libpotahcoinconsensus) (Node.js Bindings)
- [java-libpotahcoinconsensus](https://github.com/dexX7/java-libpotahcoinconsensus) (Java Bindings)
- [potahcoinconsensus-php](https://github.com/Bit-Wasp/potahcoinconsensus-php) (PHP Bindings)
