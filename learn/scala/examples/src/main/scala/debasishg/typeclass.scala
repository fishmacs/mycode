package org.fishmacs.debasishg

/**
 * type class example
 * Created by zw on 15/5/22.
 */

case class Address(no: Int, street: String, city: String, state: String, zip: String)

trait LabelMaker[T] {
  def toLabel(value: T): String
}

// Adaptor
class AddressLabelMaker extends LabelMaker[Address] {
  def toLabel(address: Address) = {
    import address._
    "%d %s, %s, %s - %s".format(no, street, city, state, zip)
  }
}

// type class
object LabelMaker {
  implicit object AddressLabelMaker extends LabelMaker[Address] {
    def toLabel(address: Address): String = {
      import address._
      "%d %s, %s, %s - %s".format(no, street, city, state, zip)
    }
  }
}

object Test {
  // def printLabel[T](t: T)(lm: LabelMaker[T]) = lm.toLabel(t)
  // same with above
  def printLabel[T: LabelMaker](t: T) = implicitly[LabelMaker[T]].toLabel(t)
}

