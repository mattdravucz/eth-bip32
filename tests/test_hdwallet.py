import unittest
from eth_bip32 import HDWallet

class TestHDWallet(unittest.TestCase):
    def test_derive_address(self):
        xpub = "xpub6CqGnXKKteadngNJV3YFVCawwJL2nzBkRj7VYZRSAsLpdmLZ4WnRKhqYZaXbqDtWqqAdyuQCMnV2ECgzRFMNiskHscRg51XN5iVzMvgRtdt"
        path = "m/0/1/1/0"
        expected_address = "0x12771330cdaee396B6fF74A1737dD482915F11b4"

        wallet = HDWallet(xpub)
        derived_wallet = wallet.from_path(path)
        derived_address = derived_wallet.address()

        self.assertEqual(derived_address.lower(), expected_address.lower(),
                         f"Derived address {derived_address} does not match expected address {expected_address}")

if __name__ == '__main__':
    unittest.main()