import sbt._
import sbt.Keys._

object ProginscalaBuild extends Build {

  lazy val proginscala = Project(
    id = "proginscala",
    base = file("."),
    settings = Project.defaultSettings ++ Seq(
      name := "ProgInScala",
      organization := "org.fish.macs",
      version := "0.1-SNAPSHOT",
      scalaVersion := "2.12.10"
      // add other settings here
    )
  )
}
