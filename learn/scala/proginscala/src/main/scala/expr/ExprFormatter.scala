package org.fishmacs.expr

import scala.collection.mutable.Stack

import org.fishmacs.layout2d.Element
import org.fishmacs.layout2d.Element.elem


sealed abstract class Expr
case class Var(name: String) extends Expr
case class Number(num: Double) extends Expr
case class UnOp(operator: String, arg: Expr) extends Expr
case class BinOp(operator: String, left: Expr, right: Expr) extends Expr

class ExprFormatter {
  private val opGroups = Array(
    Set("|", "||"),
    Set("&", "&&"),
    Set("^"),
    Set("==", "!="),
    Set("<", "<=", ">", ">="),
    Set("+", "-"),
    Set("*", "%")
  )

  private val precedence = {
    val assocs =
      for {
        i <- 0 until opGroups.length
        op <- opGroups(i)
      } yield op -> i
    assocs.toMap
  }

  private val unaryPrecedence = opGroups.length
  private val fractionPrecedence = -1

  private val binOpStack = Stack.empty[String] //new Stack[String]  // compiler error if use Stack.empty[String]???

  private def format(e: Expr, enclPrec: Int, isRight: Boolean  = false): Element =
    e match {
      case Var(name) => elem(name)
      case Number(num) => 
        def stripDot(s: String) =
          if (s endsWith ".0") s.substring(0, s.length-2)
          else s
        elem(stripDot(num.toString))
      case UnOp(op, arg) =>
        elem(op) beside format(arg, unaryPrecedence)
      case BinOp("/", left, right) =>
        val top = format(left, fractionPrecedence)
        val bot = format(right, fractionPrecedence)
        val line = elem('-', top.width max bot.width, 1)
        val frac = top above line above bot
        if (enclPrec != fractionPrecedence) frac
        else elem(" ") beside frac beside elem(" ")
      case BinOp(op, left, right) =>
        val lastOp:String = if (binOpStack.size>0) binOpStack.pop else ""
        binOpStack.push(op)
        val opPrec = precedence(op)
        val l = format(left, opPrec)
        val r = format(right, opPrec + 1, isRight=true)
        val oper = l beside elem(" " + op + " ") beside r

        if (enclPrec <= opPrec || op==lastOp && op!="-") oper
        else elem("(") beside oper beside elem(")")
    }

  def format(e: Expr): Element = format(e, 0)
}
