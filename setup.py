from setuptools import setup, Extension, find_packages

keccak256_module = Extension('eth_bip32.keccak._keccak256',
                             sources=['src/eth_bip32/keccak/keccak256.c', 'src/eth_bip32/keccak/keccak256_module.c'],
                             include_dirs=['src/eth_bip32/keccak'])

setup(
    name="eth_bip32",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[keccak256_module],
    install_requires=[
        "ecdsa",
    ],
)