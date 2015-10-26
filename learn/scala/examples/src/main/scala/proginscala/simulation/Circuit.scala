package org.fishmacs.simulation

import scala.actors.Actor
import ParallelSimulation._

class Circuit {
  val clock = new Clock

  case class SetSignal(sig: Boolean)
  case class SignalChanged(wire: Wire, sig: Boolean)

  val WireDelay = 1
  val InverterDelay = 2
  val OrGateDelay = 3
  val AndGateDelay = 3

  class Wire(name: String, init: Boolean) extends Simulant {
    def this(name: String) { this(name, false) }
    def this() { this("unnamed") }

    val clock = Circuit.this.clock
    clock.add(this)

    private var sigVal = init

    private var observers: List[Actor] = List()

    def handleSimMessage(msg: Any) {
      msg match {
        case SetSignal(s) =>
          if (s != sigVal) {
            sigVal = s
            signalObservers()
          }
      }
    }

    def signalObservers() {
      for (obs <- observers)
        clock ! AfterDelay(
          WireDelay,
          SignalChanged(this, sigVal),
          obs)
    }

    override def simStarting() { signalObservers() }

    def addObserver(obs: Actor) {
      observers = obs :: observers
    }

    override def toString = "Wire("+ name +")"
  }

  private object DummyWire extends Wire("dummy")

  abstract class Gate(inputs: List[Wire], out: Wire) extends Simulant {
    def computeOutput(values: List[Boolean]): Boolean
    val delay: Int

    val clock = Circuit.this.clock
    clock.add(this)

    inputs foreach {_.addObserver(this)}

    var values = inputs map {_=>false}

    def handleSimMessage(msg: Any) {
      msg match {
        case SignalChanged(w, sig) =>
          values = (inputs,values).zipped.map {(in,v)=>if(in==w) sig else v}
          clock ! AfterDelay(delay,
              SetSignal(computeOutput(values)),
              out)
      }
    }
  }

  def orGate(in1: Wire, in2: Wire, output: Wire) =
    new Gate(List(in1, in2), output) {
      val delay = OrGateDelay
      def computeOutput(values: List[Boolean]) = (false /: values) {_||_}
    }

  def andGate(in1: Wire, in2: Wire, output: Wire) =
    new Gate(List(in1, in2), output) {
      val delay = AndGateDelay
      def computeOutput(values: List[Boolean]) = (true /: values) {_&&_}
    }

  def inverter(input: Wire, output: Wire) =
    new Gate(List(input), output) {
      val delay = InverterDelay
      def computeOutput(values: List[Boolean]) = !values(0)
    }

  def probe(wire: Wire) = new Simulant {
    val clock = Circuit.this.clock
    clock.add(this)
    wire.addObserver(this)

    def handleSimMessage(msg: Any) {
      msg match {
        case SignalChanged(w, s) =>
           println("signal "+ w +" changed to "+ s)
      }
    }
  }

  def start() { clock ! Start }
}
