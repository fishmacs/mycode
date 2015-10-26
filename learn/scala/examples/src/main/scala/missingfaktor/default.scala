package org.fishmacs.missingfaktor

// type class

trait Default[A] {
  def value: A
}

trait LowPriorityImplicitsForDefault {
  this: Default.type =>
  implicit def forAnyRef[A](implicit ev: Null <:< A) =
    Default withValue (null: A)
}

object Default extends LowPriorityImplicitsForDefault {
  def withValue[A](a: A) = new Default[A] {
    def value = a
  }

  implicit val forBoolean = withValue(false)
  implicit val forChar = withValue(' ')
  implicit val forString = withValue("")
  implicit def forOption[A] = withValue(None: Option[A])
  implicit def forNumeric[A](implicit n: Numeric[A]) = withValue(n.zero)

  def default[A: Default] = implicitly[Default[A]].value
}

case class Complex(real: Double, imagenry: Double)

object Complex {
  implicit val default = Default withValue Complex(0.0, 0.0)
}

