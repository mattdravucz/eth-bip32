import ctypes
import os
import sys
import glob

def find_library():
    current_dir = os.path.dirname(__file__)
    pattern = os.path.join(current_dir, '_keccak256*')
    matches = glob.glob(pattern)
    
    print(f"Searching for library in: {current_dir}")
    print(f"Found matches: {matches}")
    
    if matches:
        return matches[0]
    return None

try:
    lib_path = find_library()
    print(f"Attempting to load library from: {lib_path}")
    if lib_path is None:
        raise ImportError("Cannot find the _keccak256 library.")
    libkeccak256 = ctypes.CDLL(lib_path)
    print("Library loaded successfully")
except Exception as e:
    print(f"Error loading _keccak256 library: {e}")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    raise

class SHA3_CTX(ctypes.Structure):
    _fields_ = [
        ("hash", ctypes.c_uint64 * 25),
        ("message", ctypes.c_uint64 * 24),
        ("rest", ctypes.c_uint16),
    ]

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