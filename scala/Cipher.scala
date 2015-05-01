import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.IvParameterSpec

import javax.crypto.KeyGenerator
import java.security.SecureRandom;


def getCipher(mode: String) = {
  val cipher = Cipher getInstance "AES/CBC/NoPadding"
  val skey = new SecretKeySpec(key, "AES")
  val m = if (mode=="encrypt") Cipher.ENCRYPT_MODE else Cipher.DECRYPT_MODE
  cipher.init(m, skey, new IvParameterSpec(iv))
  cipher
}

def encrypt(s: String): Array[Byte] = {
  val cipher = Cipher getInstance "AES/CBC/NoPadding"
  val skey = new SecretKeySpec(getRawKey(key), "AES")
  cipher.init(Cipher.ENCRYPT_MODE, skey, new IvParameterSpec(iv))
  cipher.doFinal(s getBytes "UTF8")
}

def encrypt1(s: String): Array[Byte] = {
  val cipher = Cipher getInstance "AES/CBC/NoPadding"
  val skey = new SecretKeySpec(key, "AES")
  cipher.init(Cipher.ENCRYPT_MODE, skey, new IvParameterSpec(iv))
  cipher.doFinal(s getBytes "UTF8")
}

def decrypt(bs: Array[Byte]): Array[Byte] = {
  val cipher = Cipher getInstance "AES/CBC/NoPadding"
  val skey = new SecretKeySpec(key, "AES")
  cipher.init(Cipher.DECRYPT_MODE, skey, new IvParameterSpec(iv))
  cipher.doFinal(bs)
}

def getRawKey(key: Array[Byte]): Array[Byte] = {
  val sr = SecureRandom.getInstance("SHA1PRNG")
  sr.setSeed(key)
  val kg = KeyGenerator.getInstance("AES")
  kg.init(128, sr)
  val k = kg.generateKey
  k.getEncoded
}
