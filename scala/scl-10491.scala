// This code fails to infer that summon(x) returns an HX
// and summon(y) returns an HY
// https://youtrack.jetbrains.com/issueMobile/SCL-10491

object singletonTypes {
  case class S1[A](id: Int)

  val x = S1[String](1)
  val y = S1[Int](2)

  trait H[T]
  trait HFactory[S <: S1[_]] {
    type T
    type H1 <: H[T]
    def create(t: T): H1
  }

  case class HX(value: String) extends H[String] {
    def x = "foo"
  }

  case class HY(value: Int) extends H[Int] {
    def y = "bar"
  }

  implicit val hfX: HFactory[x.type] { type H1 = HX } = new HFactory[x.type] {
    override type T = String
    override def create(t: String) = HX(t)
    override type H1 = HX
  }

  implicit val hfY: HFactory[y.type] { type H1 = HX} = new HFactory[y.type] {
    override type H1 = HX
    override type T = Int
    override def create(t: Int) = HY(t)
  }

  def summon[A](s1: S1[A])(implicit ev: HFactory[s1.type]): ev.H1 = {
    ev.create(???)
  }

  val shouldBeFoo: String = summon(x).x
  val shouldBeBar: String = summon(y).y
}
