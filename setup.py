from setuptools import setup, Extension, find_packages
import sys

extra_compile_args = []
extra_link_args = []

if sys.platform == 'win32':
    extra_compile_args.append('/DWIN32')
    extra_link_args.append('/MANIFEST')

keccak256_module = Extension('eth_bip32.keccak._keccak256',
                             sources=['src/eth_bip32/keccak/keccak256.c'],
                             include_dirs=['src/eth_bip32/keccak'],
                             extra_compile_args=extra_compile_args,
                             extra_link_args=extra_link_args)

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