import org.scalatestplus.play._
import play.api.test._
import play.api.test.Helpers._
import play.api.libs.json._

import models.Item
import controllers.routes.Items

class HttpSpec extends PlaySpec with OneAppPerSuite {
  var id = 0L

  val readItem: Reads[Item] = Json.reads[Item]

  "Item controller" should {
    "list item: empty" in {
      val res = route(app, FakeRequest(Items.list())).get
      status(res) mustBe OK
      val items = contentAsJson(res)
      items mustBe Json.arr()
    }

    "create item" in {
      val call = Items.create()
      val res = route(app, FakeRequest(call.method, call.url,
        FakeHeaders(Seq("Content-type" -> "application/json")),
        """{"name": "Play Framework Essentials", "price": 42}"""))
        .get
      status(res) mustBe OK
      val item = readItem.reads(contentAsJson(res)).get
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 42
      id = item.id
    }

    "list item: not empty" in {
      val res = route(app, FakeRequest(Items.list())).get
      status(res) mustBe OK
      val items = contentAsJson(res)
      items.asInstanceOf[JsArray].value must have length 1
    }

    "update item" in {
      val call = Items.update(id)
      val res = route(app, FakeRequest(call.method, call.url,
        FakeHeaders(Seq("Content-type" -> "application/json")),
        """{"name": "Play Framework Essentials", "price": 40}"""))
        .get
      status(res) mustBe OK
      val item = readItem.reads(contentAsJson(res)).get
      item.name mustBe "Play Framework Essentials"
      item.price mustBe 40
    }

    "delete item" in {
      val res = route(app, FakeRequest(Items.delete(id))).get
      status(res) mustBe OK
      contentAsString(res) mustBe "ok"
    }

    "list item: empty again" in {
      val res = route(app, FakeRequest(Items.list())).get
      status(res) mustBe OK
      val items = contentAsJson(res)
      items.asInstanceOf[JsArray].value must have length 0
    }
  }
}
