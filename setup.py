from setuptools import setup, Extension, find_packages


with open("README.md", "rt") as fh:
    long_description = fh.read()

keccak256_module = Extension('eth_bip32.keccak._keccak256',
                             sources=['src/eth_bip32/keccak/keccak256.c', 'src/eth_bip32/keccak/keccak256_module.c'],
                             include_dirs=['src/eth_bip32/keccak'])

setup(
    name="eth_bip32",
    version="0.1.1",
    description="Deriving Ethereum addresses from HD wallets using extended public keys (xpub)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[keccak256_module],
    install_requires=[
        "ecdsa",
    ],
)