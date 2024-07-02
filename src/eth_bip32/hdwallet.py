import hashlib
import hmac
import ecdsa

from eth_bip32.keccak._keccak256 import keccak256


BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def sha256(data):
    return hashlib.sha256(data).digest()

def b58decode(s):
    num = sum(BASE58_ALPHABET.index(c) * 58**i for i, c in enumerate(s[::-1]))
    return num.to_bytes((num.bit_length() + 7) // 8, 'big')

def b58decode_check(s):
    decoded = b58decode(s)
    if sha256(sha256(decoded[:-4]))[:4] != decoded[-4:]:
        raise ValueError("Invalid checksum")
    return decoded[:-4]

def derive_child_public_key(parent_public_key, parent_chain_code, index):
    data = parent_public_key + index.to_bytes(4, 'big')
    i = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
    il, ir = i[:32], i[32:]
    
    curve = ecdsa.SECP256k1
    point = ecdsa.VerifyingKey.from_string(parent_public_key, curve=curve).pubkey.point
    child_point = point + curve.generator * int.from_bytes(il, 'big')
    
    child_public_key = ecdsa.VerifyingKey.from_public_point(child_point, curve=curve).to_string("compressed")
    return child_public_key, ir

def checksum_encode(address):
    address = address.lower().replace("0x", "")
    keccak_hash = keccak256(bytes(address, encoding='utf-8')).hex()
    return "0x" + ''.join(c.upper() if int(keccak_hash[i], 16) >= 8 else c for i, c in enumerate(address))

class HDWallet:
    def __init__(self, xpub):
        data = b58decode_check(xpub)
        self.chain_code = data[13:45]
        self.public_key = data[45:]
        self.path = None

    def from_path(self, path):
        indices = [int(i) for i in path.split('/') if i.isnumeric()]
        derived = self
        derived.path = path.rstrip('/')
        for index in indices:
            derived.public_key, derived.chain_code = derive_child_public_key(derived.public_key, derived.chain_code, index)
        return derived

    def address(self):
        uncompressed = ecdsa.VerifyingKey.from_string(self.public_key, curve=ecdsa.SECP256k1).to_string("uncompressed")[1:]
        address = keccak256(uncompressed)[-20:].hex()
        return checksum_encode(address)
