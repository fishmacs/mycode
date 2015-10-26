package org.fishmacs.scalaindepth.syncutil

// 7.3

import java.io.InputStream

trait FileLike {
  def name: String
  def exists: Boolean
  def isDirectory: Boolean
  def children: Seq[FileLike]
  def child(name: String): FileLike
  def mkdirs(): Unit
  def content: InputStream
  def writeContent(otherContent: InputStream): Unit
}

object SynchUtil {
  def synchronize(from: FileLike, to: FileLike) {
    def synchronizeFile(file1: FileLike, file2: FileLike) {
      file2.writeContent(file1.content)
    }
    def synchronizeDirectory(dir1: FileLike, dir2: FileLike) {
      def findFile(file: FileLike, directory: FileLike): Option[FileLike] =
        (for(file2 <- directory.children if file.name == file2.name)
        yield file2).headOption

      for(file1 <- dir1.children) {
        val file2 = findFile(file1, dir2).getOrElse(dir2.child(file1.name))
        if(file1.isDirectory)
          file2.mkdirs()
        synchronize(file2, file1)  // a bug: wrong order!
      }
    }

    if(from.isDirectory)
      synchronizeDirectory(from, to)
    else
      synchronizeFile(from, to)
  }
}
