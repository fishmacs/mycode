import org.scalatestplus.play._
import models.{Item, Shop}
import play.api.Application
import play.api.inject.guice.GuiceApplicationBuilder
import play.api.test.FakeApplication
import play.test.WithApplication

import scala.concurrent.Await
import scala.concurrent.duration.Duration

class ShopSpec extends PlaySpec {
  val app = GuiceApplicationBuilder().build
  var id = 0L

  "A Shop" should {
    def getShop(): Shop = {
      val appToShop = Application.instanceCache[Shop]
      appToShop(app)
    }

    "add item" in new WithApplication {
      val item: Item = Await.result(getShop.create("Play Framework Essentials", 42), Duration.Inf)
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 42
      id = item.id
    }

    "get item" in new WithApplication {
      val v = Await.result(getShop.get(id), Duration.Inf)
      val item = v.get
      item mustBe a [Item]
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 42
      id = item.id
    }

    "list item" in new WithApplication {
      implicit val app0 = GuiceApplicationBuilder().build()
      val items = Await.result(getShop.list, Duration.Inf)
      items must have length 1
      items(0).name mustBe "Play Framework Essentials"
      items(0).price mustBe 42
    }

    "update item" in new WithApplication {
      implicit val app0 = GuiceApplicationBuilder().build()
      val Some(item): Option[Item] = Await.result(getShop.update(id, "Play Framework Essentials", 40), Duration.Inf)
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 40
    }

    "delete item" in new WithApplication {
      implicit val app0 = GuiceApplicationBuilder().build()
      Await.result(getShop.delete(id), Duration.Inf) mustBe true
      Await.result(getShop.list, Duration.Inf) must have length 0
    }
  }
}
