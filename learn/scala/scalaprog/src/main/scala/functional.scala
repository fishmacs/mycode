val graph = List("a", List("b1","b2","b3"), List("c1", List("c21", Nil, "c22"), Nil, "e"))

// flatten filter Nil out, and flatten List beyond one level, flatMap only flatten one level(List of List -> List)
def flatten(list: List[_]): List[_] = list flatMap {
  case head :: tail => head :: flatten(tail)
  case Nil => Nil
  case x => List(x)
}
