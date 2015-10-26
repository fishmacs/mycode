import scala.collection.generic.CanBuildFrom
import scala.collection.IndexedSeqLike
import scala.collection.mutable.Builder
import scala.collection.mutable.ArrayBuffer

final class RNA private (val groups: Array[Int], val length: Int) extends IndexedSeq[Base] with IndexedSeqLike[Base, RNA] {
  import RNA._

  override protected[this] def newBuilder: Builder[Base, RNA] = RNA.newBuilder

  def apply(idx: Int): Base = {
    if (idx < 0 || length <= idx)
      throw new IndexOutOfBoundsException
    Base.fromInt(groups(idx/N) >> (idx % N * S) & M)
  }

  override def foreach[U](f: Base => U): Unit = {
    var i = 0
    var b = 0
    while(i < length) {
      b = if (i%N == 0) groups(i/N) else b >>> S
      f(Base.fromInt(b & M))
      i += 1
    }
  }
}

object RNA {
  private val S = 2
  private val M = (1 << S) - 1
  private val N = 32 / S

  def fromSeq(buf: Seq[Base]): RNA = {
    val groups = new Array[Int]((buf.length+N-1) / N)
    for (i <- 0 until buf.length)
      groups(i/N) |= Base.toInt(buf(i)) << (i%N*S)
    new RNA(groups, buf.length)
  }

  def apply(bases: Base*) = fromSeq(bases)

  def newBuilder: Builder[Base, RNA] = new ArrayBuffer mapResult fromSeq

  implicit def canBuildFrom: CanBuildFrom[RNA, Base, RNA] =
    new CanBuildFrom[RNA, Base, RNA] {
      def apply(): Builder[Base, RNA] = newBuilder
      def apply(from: RNA): Builder[Base, RNA] = newBuilder
    }
}
