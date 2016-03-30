package org.fishmacs.jamesiry.monadio

class HelloWorld_v1 extends IOApplication_v1 {
  import RTConsole_v1._

  def iomain(args: Array[String], startState: WorldState) =
    putString(startState, "Hello world")
}

class HelloWorld_v2 extends IOApplication_v2 {
  import RTConsole_v2._

  def iomain(args: Array[String]) =
    putString("Hello world")
}

class HelloWorld_v3 extends IOApplication_v3 {
  import RTConsole_v3._

  override
  def iomain(args: Array[String]) =
    putString("hello, world")
}

class HelloWorld_v4 extends IOApplication_v4 {
  import RTConsole_v4._

  def iomain(args: Array[String]) =
    for {
      _ <- putString("This is an example of the IO monad.")
      _ <- putString("What's you name?")
      name <- getString
      _ <- putString("Hello " + name)
    } yield ()
}

object HelloWorld extends IOApplication {
  import IOAction._
  import RTConsole._

  def sayHello(n: String) = n match {
    case "Bob" => putLine("Hello, Bob")
    case "Chunk" => putLine("Hey, Chuck")
    case "Sarah" => putLine("Helloooo, Sarah")
    case _ => fail("match exception")
  }

  def ask(q: String) =
    putString(q) >> getString

  def processString(s: String) = s match {
    case "quit" => putLine("Catch ya later")
    case _ => (sayHello(s) or putLine(s + ", I don't know you.")) >> loop
  }

  def loop: IOAction[Unit] =
    for {
      name <- ask("What's your name? ");
      _ <- processString(name)
    } yield ()

  def iomain(args: Array[String]) = {
    putLine("This is an example of the IO monad.") >>
    putLine("Enter a name or 'quit'") >>
    loop
  }
}
