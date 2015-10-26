package org.fishmacs.scalaindepth.typeclass1

import java.text.Collator
import java.util.Locale

// https://blog.safaribooksonline.com/2013/05/28/scala-type-classes-demystified/

trait Comparable[T] {
  def <=(other: T): Boolean
}

trait CanCompare[T] {
  def compare(a: T, b: T): Boolean
}

object CanCompare {
  implicit object SpanishString extends CanCompare[String] {
    val collator = Collator.getInstance(new Locale("ES"))
    def compare(a: String, b: String) = collator.compare(a, b) <= 0
  }
}

object Test {
  implicit def order(a: T)(implicit c: CanCompare[T]) =
    new Comparable[T] {
      def <=(b: T) = c.compare(a, b)
    }
}
