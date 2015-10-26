package org.fishmacs.neophyte

// type class

object Math {
  import annotation.implicitNotFound

  @implicitNotFound("No member of type class NumberLike in scope for ${T}")
  trait NumberLike[T] {
    def plus(x: T, y: T): T
    def divide(x: T, y: Int): T
    def minus(x: T, y: T): T
  }

  object NumberLike {
    implicit object NumberDouble extends NumberLike[Double] {
      def plus(x: Double, y: Double): Double = x + y
      def divide(x: Double, y: Int): Double = x / y
      def minus(x: Double, y: Double): Double = x - y
    }

    implicit object NumberLikeInt extends NumberLike[Int] {
      def plus(x: Int, y: Int): Int = x + y
      def divide(x: Int, y: Int): Int = x / y
      def minus(x: Int, y: Int): Int = x - y
    }
  }
}

object Statistics {
  import Math.NumberLike

  // def mean[T](xs: Vector[T])(implicit ev: NumberLike[T]): T =
  //   ev.divide(xs.reduce(ev.plus(_, _)), xs.size)

  def mean[T: NumberLike](xs: Vector[T]): T = {
    val ev = implicitly[NumberLike[T]]
    ev.divide(xs.reduce(ev.plus(_, _)), xs.size)
  }

  def median[T: NumberLike](xs: Vector[T]): T = xs(xs.size / 2)

  def quartiles[T: NumberLike](xs: Vector[T]): (T, T, T) =
    (xs(xs.size / 4), median(xs), xs(xs.size / 4 * 3))

  def iqr[T: NumberLike](xs: Vector[T]): T =
    quartiles(xs) match {
      case (lowerQuartile, _, upperQuartile) =>
        implicitly[NumberLike[T]].minus(upperQuartile, lowerQuartile)
    }
}
