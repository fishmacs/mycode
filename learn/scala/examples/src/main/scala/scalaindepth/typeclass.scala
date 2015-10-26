package org.fishmacs.scalaindepth.typeclass

// 7.3

import java.io.{FileInputStream, File, InputStream}

trait FileLike[T] {
  def name(file: T): String
  def exists(file: T): Boolean
  def isDirectory(file: T): Boolean
  def children(directory: T): Seq[T]
  def child(parent: T, name: String): T
  def parent(file: T): T
  def mkdirs(file: T)
  def content(file: T): InputStream
  def writeContent(file: T, otherContent: InputStream)
}

object FileLike {
  implicit val ioFileLike = new FileLike[File] {
    override def name(file: File) = file.getName()
    override def isDirectory(file: File) = file.isDirectory()
    override def parent(file: File) = file.getParentFile()
    override def children(directory: File) = directory.listFiles()
    override def child(parent: File, name: String) = new File(parent, name)
    override def mkdirs(file: File) = file.mkdirs()
    override def content(file: File) = new FileInputStream(file)
    override def writeContent(file: File, otherContent: InputStream) {}
    override def exists(file: File) = file.exists()
  }
}

object SynchUtil {
  def synchronize1[F: FileLike, T: FileLike](from: F, to: T) {
    val fromHelper = implicitly[FileLike[F]]
    val toHelper = implicitly[FileLike[T]]

    def synchronizeFile(file1: F, file2: T) {
      toHelper.writeContent(file2, fromHelper.content(file1))
    }

    def synchronizeDirectory(dir1: F, dir2: T) {
      def findFile(file: F, directory: T): Option[T] =
        (for(file2 <- toHelper.children(directory)
          if fromHelper.name(file) == toHelper.name(file2)
        ) yield file2).headOption

      for (file1 <- fromHelper.children(dir1)) {
        val file2 = findFile(file1, dir2).getOrElse(toHelper.child(dir2, fromHelper.name(file1)))
        if(fromHelper.isDirectory(file1))
          toHelper.mkdirs(file2)
        synchronize1[F, T](file1, file2)
      }
    }

    if(fromHelper.isDirectory(from))
      synchronizeDirectory(from, to)
    else
      synchronizeFile(from, to)
  }
}
