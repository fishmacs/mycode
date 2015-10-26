package org.fishmacs.expr

/**
 * Created with IntelliJ IDEA.
 * User: zw
 * Date: 13-6-3
 * Time: 12:34 AM
 * To change this template use File | Settings | File Templates.
 */
object Express extends Application {
  val f = new ExprFormatter
  
  val e1 = BinOp("*", BinOp("/", Number(1), Number(2)),
                      BinOp("+", Var("x"), Number(1)))
  val e2 = BinOp("+", BinOp("/", Var("x"), Number(2)),
                      BinOp("/", Number(1.5), Var("x")))
  val e3 = BinOp("/", e1, e2)

  val e4 = BinOp("+", BinOp("+", Number(0), Number(1)), BinOp("+", Number(2), Number(3)))
  val e5 = BinOp("-", BinOp("-", Number(0), Number(1)), BinOp("-", Number(2), Number(3)))

  def show(e: Expr) = println(f.format(e)+ "\n\n")
  
  for (e <- Array(e1, e2, e3, e4, e5)) show(e)
}
