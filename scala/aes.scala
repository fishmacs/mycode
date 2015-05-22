import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.IvParameterSpec

import javax.crypto.KeyGenerator
import java.security.SecureRandom;

val iv = Array[Byte](0x12, 0x34, 0x56, 0x78, 0x90, 0xab, 0xcd, 0xef, 0x12, 0x34, 0x56, 0x78, 0x90, 0xab, 0xcd, 0xef) map {_.asInstanceOf[Byte]}

//val key = Array[Int](0xc5, 0xfc, 0xa2, 0x90, 0x2a, 0x77, 0x45, 0x7c, 0x55, 0x93, 0xd2, 0x2d, 0x09, 0xae, 0x58, 0xa8) map {_.asInstanceOf[Byte]}

val key = Array[Int](0x12, 0x34, 0x56, 0x78, 0x90, 0x12, 0x34, 0x56, 0x78, 0x90, 0x12, 0x34, 0x12, 0x34, 0x56, 0x78) map {_.asInstanceOf[Byte]}

//"c5fca2902a77457c5593d22d09ae58a8"

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
