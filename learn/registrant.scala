import scala.io.Source._

case class Registrant(line: String) {
  val data = line.split(",")
  val first = data(0)
  val last = data(1)
  val email = data(2)
  val payment = data(3).toDouble
}

val data = """Bob,Dobbs,bob@dobbs.com,25.00
Rocket J.,Squirrel,rocky@frostbite.com,0.00
Bullwinkle,Moose,bull@frostbite.com,0.25
Vim,Wibner,vim32@goomail.com,25.00"""

val lines = fromString(data).getLines
//val lines = fromString(data).getLines.toIndexedSeq
val registrants = lines.map(Registrant)
registrants.foreach(println)
registrants.foreach(println)
