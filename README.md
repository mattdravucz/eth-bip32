# HD Wallet Ethereum Address Derivation

This Python script provides functionality to derive Ethereum addresses from an extended public key (xpub) using Hierarchical Deterministic (HD) wallet principles.

## Motivation

While there are existing libraries for HD wallet operations, I couldn't find a fast, lightweight solution specifically for deriving Ethereum addresses from an xpub. This script aims to fill that gap, providing a simple and efficient way to generate Ethereum addresses from a given xpub and derivation path.

## Features

- Decode base58-encoded xpub
- Derive child public keys from parent public keys and chain codes
- Generate Ethereum addresses from derived public keys
- Support for custom derivation paths

## Usage

```python
xpub = "xpub6CqGnXKKteadngNJV3YFVCawwJL2nzBkRj7VYZRSAsLpdmLZ4WnRKhqYZaXbqDtWqqAdyuQCMnV2ECgzRFMNiskHscRg51XN5iVzMvgRtdt"
path = "m/0/1/1/0"

wallet = HDWallet(xpub)
derived_wallet = wallet.derive_path(path)
ethereum_address = derived_wallet.eth_address()
print(f"Derived Ethereum address: {ethereum_address}")
```

## Dependencies

- `hashlib`
- `hmac`
- `ecdsa`
- `eth_utils`

## Credits

This implementation was inspired by and references concepts from the following libraries:

- [pycoin](https://github.com/richardkiss/pycoin)
- [hdwallet](https://github.com/meherett/python-hdwallet)
- [ethers](https://github.com/ethers-io/ethers.py)

## License

TBD
