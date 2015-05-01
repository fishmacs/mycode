import unittest
from unittest import TestCase

import cipher


class CipherTest(TestCase):
    def test_aes(self):
        mycipher = cipher.Cipher('aes', '1' * 16, '1' * 16)
        encrypted = mycipher.encrypt('abc', final=True)
        self.assertEqual(16, len(encrypted))
        to_encrypt = 'a' * 16
        encrypted = mycipher.encrypt(to_encrypt, padding=False, final=True)
        self.assertEqual(to_encrypt, mycipher.decrypt(encrypted, padding=False))
        mycipher.end()
        self.assertEqual('abc', mycipher.decrypt(mycipher.encrypt('abc', final=True)))

    def test_des(self):
        mycipher = cipher.Cipher('des3', '1' * 16, '1' * 8)
        encrypted = mycipher.encrypt('abc', final=True)
        self.assertEqual(8, len(encrypted))
        to_encrypt = 'a' * 8
        encrypted = mycipher.encrypt(to_encrypt, padding=False, final=True)
        self.assertEqual(to_encrypt, mycipher.decrypt(encrypted, padding=False))
        mycipher.end()
        self.assertEqual('abc', mycipher.decrypt(mycipher.encrypt('abc', final=True)))

if __name__ == '__main__':
    unittest.main()
    