package org.fishmacs.simulation

trait Adders extends Circuit {
  def halfAdder(a: Wire, b: Wire, s: Wire, c: Wire) {
    val d, e = new Wire
    orGate(a, b, d)
    andGate(a, b, c)
    inverter(c, e)
    andGate(d, e, s)
  }

  def fullAdder(a: Wire, b: Wire, cin: Wire,
                sum: Wire, cout: Wire) {
    val s, c1, c2 = new Wire
    halfAdder(a, cin, s, c1)
    halfAdder(b, s, sum, c2)
    orGate(c1, c2, cout)
  }
}

object Demo {
  def main(args: Array[String]) {
    val circuit = new Circuit with Adders
    import circuit._
    val ain = new Wire("ain", true)
    val bin = new Wire("bin", false)
    val cin = new Wire("cin", true)
    val sout = new Wire("sout")
    val cout = new Wire("cout")
    probe(ain)
    probe(bin)
    probe(cin)
    probe(sout)
    probe(cout)
    fullAdder(ain, bin, cin, sout, cout)
    circuit.start()
  }
}
