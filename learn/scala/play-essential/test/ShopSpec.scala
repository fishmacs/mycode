import org.scalatestplus.play._

import models.{Shop}

class ShopSpec extends PlaySpec with OneAppPerTest {
  var id = 0L

  "A Shop" should {
    "add item" in {
      val Some(item) = Shop.create("Play Framework Essentials", 42)
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 42
      id = item.id
    }

    "list item" in {
      val items = Shop.list 
      items must have length 1
      items(0).name mustBe "Play Framework Essentials"
      items(0).price mustBe 42
    }

    "update item" in {
      val Some(item) = Shop.update(id, "Play Framework Essentials", 40)
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 40
    }

    "delete item" in {
      Shop.delete(id) mustBe true
      Shop.list must have length 0
    }
  }
}
