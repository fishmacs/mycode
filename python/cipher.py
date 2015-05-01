import pkcs7

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7


class Cipher(object):
    def __init__(self, algo, key, iv, mode=MODE_CBC):
        self.algo = algo
        self.key = key
        self.iv = iv
        self.mode = mode
        self.cipher = None
        self.padder = None

    def encrypt(self, s, padding=True, final=False):
        if not self.cipher:
            self.cipher = self._get_cipher(padding)
        if padding:
            s = self.padder.encode(s)
        ret = self.cipher.encrypt(s)
        if final:
            self.cipher = None
        return ret

    def decrypt(self, s, padding=True, final=False):
        if not self.cipher:
            self.cipher = self._get_cipher(padding)
        ret = self.cipher.decrypt(s)
        if padding:
            ret = self.padder.decode(ret)
        if final:
            self.cipher = None
        return ret

    def end(self):
        self.cipher = None

    def _get_cipher(self, padding):
        if self.algo == 'aes':
            from Crypto.Cipher import AES
            if padding:
                self.padder = pkcs7.PKCS7Encoder(16)
            return AES.new(self.key, self.mode, self.iv)
        elif self.algo == 'des3':
            from Crypto.Cipher import DES3
            if padding:
                self.padder = pkcs7.PKCS7Encoder(8)
            return DES3.new(self.key, self.mode, self.iv)
        else:
            return ValueError('Unknown algorithm: ' + self.algo)
            
        