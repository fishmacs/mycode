package org.fishmacs.scalaindepth.syncutil1

// 7.3

import java.io.InputStream

// modify trait FileLike to use type parameter
trait FileLike[X <: FileLike[X]] {
  def name: String
  def exists: Boolean
  def isDirectory: Boolean
  def children: Seq[X]
  def child(name: String): X
  def mkdirs(): Unit
  def content: InputStream
  def writeContent(otherContent: InputStream): Unit
}

object SynchUtil {
  // ensure correct order with different from/to types
  def synchronize[F <: FileLike[F], T <: FileLike[T]](from: F, to: T) {
    def synchronizeFile(file1: F, file2: T) {
      file2.writeContent(file1.content)
    }

    def synchronizeDirectory(dir1: F, dir2: T) {
      def findFile(file: F, directory: T): Option[T] =
        (for(file2 <- directory.children if file.name == file2.name
        ) yield file2).headOption

      for (file1 <- dir1.children) {
        val file2 = findFile(file1, dir2).getOrElse(dir2.child(file1.name))
        if(file1.isDirectory)
          file2.mkdirs()
        synchronize[F, T](file1, file2)  // compilation failure even order correct!
      }
    }

    if(from.isDirectory)
      synchronizeDirectory(from, to)
    else
      synchronizeFile(from, to)
  }
}
