
**HD Wallet**
================

A Python implementation of a Hierarchical Deterministic (HD) wallet for Ethereum.

**Usage**
--------

### Importing the Module

To use the HD wallet, simply import the module:
```python
import hdwallet
```
### Creating an HD Wallet

Create an instance of the `HDWallet` class, specifying the symbol of the cryptocurrency (e.g., "ETH" for Ethereum):
```python
wallet = HDWallet(symbol="ETH")
```
### Deriving an HD Wallet from an Extended Public Key

Derive an HD wallet from an extended public key (xpub) using the `from_xpublic_key` method:
```python
xpub = "xpub6CqGnXKKteadngNJV3YFVCawwJL2nzBkRj7VYZRSAsLpdmLZ4WnRKhqYZaXbqDtWqqAdyuQCMnV2ECgzRFMNiskHscRg51XN5iVzMvgRtdt"
wallet.from_xpublic_key(xpub)
```
### Deriving a Child Wallet

Derive a child wallet from the current wallet using the `derive_path` method, specifying the derivation path (e.g., "m/0/1/1/0"):
```python
derived_wallet = wallet.derive_path("m/0/1/1/0")
```
### Getting the P2PKH Address

Get the P2PKH address of the derived wallet using the `p2pkh_address` method:
```python
ethereum_address = derived_wallet.p2pkh_address()
print(f"Derived Ethereum address: {ethereum_address}")
```
### Debugging Information

Get debugging information about the wallet using the `debug_info` method:
```python
wallet.debug_info()
```
**Functions**
--------------

### `sha256(data)`

Compute the SHA-256 hash of the input data.

### `ripemd160(data)`

Compute the RIPEMD-160 hash of the input data.

### `b58encode(v)`

Encode the input data using Base58.

### `b58decode(s)`

Decode the input Base58 string.

### `b58decode_check(s)`

Decode the input Base58 string and verify the checksum.

### `derive_child_public_key(parent_public_key, parent_chain_code, index)`

Derive a child public key from the parent public key and chain code using the specified index.

### `checksum_encode(address)`

Encode the input address with a checksum.

**Classes**
---------

### `HDWallet`

The HD wallet class, which represents a hierarchical deterministic wallet.

**Constants**
------------

### `BASE58_ALPHABET`

The Base58 alphabet used for encoding and decoding.

**Dependencies**
--------------

* `hashlib` for cryptographic hash functions
* `hmac` for keyed-hash message authentication
* `ecdsa` for elliptic curve digital signatures
* `eth_utils` for Ethereum-specific utility functions