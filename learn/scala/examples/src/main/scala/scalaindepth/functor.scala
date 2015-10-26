package org.fishmacs.scalaindepth.functor

// https://blog.safaribooksonline.com/2013/05/28/scala-type-classes-demystified/

import java.util.ArrayList

trait Functor[F[_]] {
  def map[X, Y](f: X => Y): F[X] => F[Y]
}

object Functor {
  implicit object JALtoFunctor extends Functor[ArrayList] {
    def map[X, Y](f: X => Y) = (xs: ArrayList[X]) => {
      val ys = new ArrayList[Y]
      for(i <- 0 until xs.size) ys.add(f(xs get i))
      ys
    }
  }
}

object Test {
  implicit def fops[F[_]: Functor, A](fa: F[A]) = new {
    val witness = implicitly[Functor[F]]
    final def map[B](f: A => B): F[B] = witness.map(f)(fa)
  }
}
