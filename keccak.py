import ctypes
import binascii

# Load the shared library
libkeccak256 = ctypes.CDLL('./libkeccak256.so')

# Define the SHA3_CTX structure (as per keccak256.h)
class SHA3_CTX(ctypes.Structure):
    _fields_ = [
        ("hash", ctypes.c_uint64 * 25),
        ("message", ctypes.c_uint64 * 24),
        ("rest", ctypes.c_uint16),
    ]

# Define function prototypes
libkeccak256.keccak_init.argtypes = [ctypes.POINTER(SHA3_CTX)]
libkeccak256.keccak_update.argtypes = [ctypes.POINTER(SHA3_CTX), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint16]
libkeccak256.keccak_final.argtypes = [ctypes.POINTER(SHA3_CTX), ctypes.POINTER(ctypes.c_ubyte)]

# Python wrapper for keccak256
def keccak256(data):
    ctx = SHA3_CTX()
    libkeccak256.keccak_init(ctypes.byref(ctx))
    libkeccak256.keccak_update(ctypes.byref(ctx), (ctypes.c_ubyte * len(data)).from_buffer_copy(data), len(data))
    result = (ctypes.c_ubyte * 32)()
    libkeccak256.keccak_final(ctypes.byref(ctx), result)
    return bytes(result)

