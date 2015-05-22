import javax.crypto.{Cipher => jCipher}
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.IvParameterSpec

import javax.crypto.KeyGenerator
import java.security.SecureRandom;

class PKCS7(paddingLen: Int=8) {
  def encode(src: Array[Byte]): Array[Byte] = {
    val padding = paddingLen - (b.length % paddingLen)
    src ++ Array.fill(padding)(padding)
  }

  def decode(src: Array[Byte]): Array[Byte] = {
    src take (src.length - src.last)
  }
}

class Cipher(algo: String, key: Array[Byte], iv: Array[Byte], mode: String="cbc") {
  var mEncrypter: JCipher = null
  var mDecrypter: JCipher = null
  var mPadder: PKCS7 = null

  def encrypt(b: Array[Byte], padding: Boolean=True, end: Boolean=True): Array[Byte] = {
    if (mEncrypter == null)
      mEncrypter = getCipher("encrypt", padding)
    var src = b
    if (padding)
      src = padder encode src
    if (end)
      mEncrypter.doFinal(src)
    else
      mEncrypter.update(src)
  }

  def decrypt(b: Array[Byte], padding: Boolean=True, end: Boolean=True): Array[Byte] = {
    if (mDecrypter == null)
      mDecrypter = getCipher("decrypt", padding)
    val encrypted = 
      if (end)
        mEncrypter.doFinal(b)
      else
        mEncrypter.update(b)
    if (padding)
      padder decode encrypted
    else
      encrypted
  }

  def getCipher(opMode: String, padding: Boolean): JCipher = {
    val initStr = "%s/%s/NoPadding".format(algo, mode).toUpperCase
    val cipher = JCipher getInstance initStr
    val secretKey = new SecretKeySpec(key, algo)
    val cipherMode = opMode match {
      case "encrypt" => JCipher.ENCRYPT_MODE
      case "decrypt" => JCipher.DECRYPT_MODE
      case _ => throw new IllegalArgumentException("Unknown mode: " + opMode)
    }
    cipher.init(cipherMode, secretKey, new IvParameterSpec(iv))
    if (padding)
      padder = new PKCS7(algo match {
        case "aes" => 16
        case "des3" => 8
        case _ => 8
      })
    cipher
  }
}
