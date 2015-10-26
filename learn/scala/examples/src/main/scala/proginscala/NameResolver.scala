import scala.actors.Actor
import scala.actors.Actor.{actor, loop, react, self}
import java.net.{InetAddress, UnknownHostException}

object NameResolver extends Actor {
  def act() {
    react {
      case (name: String, actor: Actor) =>
        actor ! getIp(name)
        act()
      case "exit" =>
        println("Name resolver exiting")
      case msg =>
        print("Unhandled message: " + msg)
        act()
    }
  }

  def getIp(name: String): Option[InetAddress] = {
    try {
      Some(InetAddress.getByName(name))
    } catch {
      case _: UnknownHostException => None
    }
  }
}

object SillyActor2 {
  val sillyActor2 = actor {
    def emoteLater() {
      val mainActor = self
      actor {
        Thread.sleep(1000)
        mainActor ! "Emote"
      }
    }

    var emoted = 0
    emoteLater()

    loop {
      react {
        case "Emote" =>
          println("I'm acting!")
        emoted += 1
        if(emoted < 5)
          emoteLater()
        case msg =>
          println("Received:" + msg)
      }
    }
  }
}
