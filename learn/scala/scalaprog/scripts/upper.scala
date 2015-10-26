class Upper {
  def upper(strings: String*): Seq[String] = {
    strings.map(_.toUpperCase)
  }
}

val up = new Upper
// why Console.?
Console.println(up.upper("A", "First", "Scala", "Program"))
