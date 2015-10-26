package org.fishmacs.jamesiry.monadio

object RTConsole_v1 {
  def getString(state: WorldState) =
    (state.nextState, Console.readLine)

  def putString(state: WorldState, s: String) =
    (state.nextState, Console.print(s))
}

object RTConsole_v2 {
  def getString = { state: WorldState =>
    (state.nextState, Console.readLine)
  }

  def putString(s: String) = { state: WorldState =>
    (state.nextState, Console.print(s))
  }
}

object RTConsole_v3 {
  def getString = IOAction_v3(Console.readLine)

  def putString(s: String) =
    IOAction_v3(Console.print(s))
}

object RTConsole_v4 {
  def getString = IOAction_v4(Console.readLine)

  def putString(s: String) =
    IOAction_v4(Console.print(s))
}

object RTConsole {
  val getString = IOAction(Console.readLine)

  def putString(s: String) = IOAction(Console.print(s))

  def putLine(s: String) = IOAction(Console.println(s))
}
