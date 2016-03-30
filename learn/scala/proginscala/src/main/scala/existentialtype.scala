import scala.collection.mutable.Set
import java.util.Collection

abstract class SetAndType {
  type Elem
  val set: Set[Elem]
}

def javaSet2ScalaSet[T](jset: Collection[T]): SetAndType = {
  val sset = Set.empty[T]
  val iter = jset.iterator
  while(iter.hasNext)
    sset += iter.next()
  return new SetAndType {
    type Elem = T
    val set = sset
  }
}
