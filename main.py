import hashlib
import hmac
import ecdsa
from eth_utils import keccak

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def sha256(data):
    return hashlib.sha256(data).digest()

def ripemd160(data):
    return hashlib.new('ripemd160', data).digest()

def b58encode(v):
    value = int.from_bytes(v, 'big')
    result = ''
    while value:
        value, mod = divmod(value, 58)
        result += BASE58_ALPHABET[mod]
    for byte in v:
        if byte == 0:
            result += BASE58_ALPHABET[0]
        else:
            break
    return result[::-1]

def b58decode(s):
    num = 0
    for char in s:
        num *= 58
        num += BASE58_ALPHABET.index(char)
    combined = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    prefix = b'\x00' * (len(s) - len(s.lstrip(BASE58_ALPHABET[0])))
    return prefix + combined

def b58decode_check(s):
    decoded = b58decode(s)
    if len(decoded) < 4:
        raise ValueError("Invalid base58 checksum string")
    data, checksum = decoded[:-4], decoded[-4:]
    if sha256(sha256(data))[:4] != checksum:
        raise ValueError("Invalid checksum")
    return data

def derive_child_public_key(parent_public_key, parent_chain_code, index):
    if index >= 0x80000000:
        raise ValueError("Cannot derive hardened child from public key")
    
    data = parent_public_key + index.to_bytes(4, 'big')
    i = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
    il, ir = i[:32], i[32:]
    
    curve = ecdsa.SECP256k1
    point = ecdsa.VerifyingKey.from_string(parent_public_key, curve=curve).pubkey.point
    factor = int.from_bytes(il, 'big')
    child_point = point + curve.generator * factor
    
    child_public_key = ecdsa.VerifyingKey.from_public_point(child_point, curve=curve).to_string("compressed")
    return child_public_key, ir

def checksum_encode(address):
    address = address.lower().replace("0x", "")
    keccak_hash = keccak(bytes(address, encoding='utf-8')).hex()
    out = ""
    
    for i, c in enumerate(address):
        if int(keccak_hash[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
            
    return "0x" + out

class HDWallet:
    def __init__(self, symbol="ETH"):
        self.symbol = symbol
        self.depth = 0
        self.parent_fingerprint = b'\x00\x00\x00\x00'
        self.child_number = 0
        self.chain_code = None
        self.public_key = None
        self.xpub = None
        self.path = "m"

    def from_xpublic_key(self, xpub):
        data = b58decode_check(xpub)
        
        if len(data) != 78:
            raise ValueError("Invalid extended public key")

        self.xpub = xpub
        self.depth = data[4]
        self.parent_fingerprint = data[5:9]
        self.child_number = int.from_bytes(data[9:13], 'big')
        self.chain_code = data[13:45]
        self.public_key = data[45:]

    def derive_path(self, path):
        new_wallet = HDWallet(symbol=self.symbol)
        new_wallet.xpub = self.xpub
        new_wallet.depth = self.depth
        new_wallet.parent_fingerprint = self.parent_fingerprint
        new_wallet.child_number = self.child_number
        new_wallet.chain_code = self.chain_code
        new_wallet.public_key = self.public_key
        new_wallet.path = self.path

        if path.startswith('m/'):
            path = path[2:]
        
        indices = [int(i) for i in path.split('/') if i.isnumeric()]
        
        for child_index in indices:
            new_wallet.public_key, new_wallet.chain_code = derive_child_public_key(new_wallet.public_key, new_wallet.chain_code, child_index)
            new_wallet.depth += 1
            new_wallet.child_number = child_index
            new_wallet.path += f"/{child_index}"
        
        return new_wallet

    def p2pkh_address(self):
        if not self.public_key:
            raise ValueError("Public key must be set")
            
        uncompressed_pubkey = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.public_key.hex()), curve=ecdsa.SECP256k1).to_string("uncompressed")
        pub = uncompressed_pubkey[1:]
        keccak_hash = keccak(pub)
        address = keccak_hash[-20:]
        return checksum_encode(address.hex())

    def uncompressed(self):
        vk = ecdsa.VerifyingKey.from_string(self.public_key, curve=ecdsa.SECP256k1)
        return "04" + vk.to_string().hex()

    def debug_info(self):
        vk = ecdsa.VerifyingKey.from_string(self.public_key, curve=ecdsa.SECP256k1)
        uncompressed_pubkey = vk.to_string()
        print(f"Root XPublic Key: {self.xpub}")
        print(f"XPublic Key: {self.xpub}")
        print(f"Uncompressed: {uncompressed_pubkey.hex()}")
        print(f"Compressed: {self.public_key.hex()}")
        print(f"Chain Code: {self.chain_code.hex()}")
        print(f"Public Key: {self.public_key.hex()}")
        print(f"Path: {self.path}")
        print(f"P2PKH Address: {self.p2pkh_address()}\n")

if __name__ == "__main__":
    xpub = "xpub6CqGnXKKteadngNJV3YFVCawwJL2nzBkRj7VYZRSAsLpdmLZ4WnRKhqYZaXbqDtWqqAdyuQCMnV2ECgzRFMNiskHscRg51XN5iVzMvgRtdt"
    path = "m/0/1/1/0"
    
    wallet = HDWallet(symbol="ETH")
    
    wallet.from_xpublic_key(xpub)
    # wallet.debug_info()
    derived_wallet = wallet.derive_path(path)
    # derived_wallet.debug_info()
    ethereum_address = derived_wallet.p2pkh_address()
    print(f"Derived Ethereum address: {ethereum_address}")
    