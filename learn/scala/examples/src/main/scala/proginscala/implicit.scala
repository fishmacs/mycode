object ImplicitParam {
  def maxListUpBound[T <: Ordered[T]](elements: List[T]): T =
    elements match {
      case List() => throw new IllegalArgumentException("empty list!")
      case List(x) => x
      case x :: xs =>
        val maxRest = maxListUpBound(xs)
        if (x > maxRest) x else maxRest
    }

  def maxListImpParm[T](elements: List[T])(implicit orderer: T => Ordered[T]): T =
    elements match {
      case List() => throw new IllegalArgumentException("empty list!")
      case List(x) => x
      case x :: xs =>
        val maxRest = maxListImpParm(xs)(orderer)
        if (orderer(x) > maxRest) x
        else maxRest
    }

  def maxList[T](elements: List[T])(implicit orderer: T => Ordered[T]): T =
    elements match {
      case List() => throw new IllegalArgumentException("empty list!")
      case List(x) => x
      case x :: xs =>
        val maxRest = maxList(xs)
        if (x > maxRest) x else maxRest
    }

  def maxListFinal[T <% Ordered[T]](elements: List[T]): T =
    elements match {
      case List() => throw new IllegalArgumentException("empty list!")
      case List(x) => x
      case x :: xs =>
        val maxRest = maxListFinal(xs)
        if (x > maxRest) x else maxRest
    }
}