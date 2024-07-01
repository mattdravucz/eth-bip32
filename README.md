# eth-bip32

eth-bip32 is a Python package for deriving Ethereum addresses from HD wallets using extended public keys (xpub).

## Installation

You can install eth-bip32 using pip:

```
pip install eth_bip32
```

## Usage

Here's a basic example of how to use eth-bip32:

```python
from eth_bip32 import HDWallet

xpub = "xpub6CqGnXKKteadngNJV3YFVCawwJL2nzBkRj7VYZRSAsLpdmLZ4WnRKhqYZaXbqDtWqqAdyuQCMnV2ECgzRFMNiskHscRg51XN5iVzMvgRtdt"
path = "m/0/1/1/0"

wallet = HDWallet(xpub)
derived_wallet = wallet.from_path(path)
ethereum_address = derived_wallet.address()
print(f"Derived Ethereum address: {ethereum_address}")
```

## Local build

```
pip install .
```


## Test

```
python -m unittest discover -v tests
```



## License

This project is licensed under the MIT License.

## Dependencies
- `ecdsa`


## Credits

This implementation was inspired by and references concepts from the following libraries:

- [pycoin](https://github.com/richardkiss/pycoin)
- [hdwallet](https://github.com/meherett/python-hdwallet)
- [ethers](https://github.com/ethers-io/ethers.py)