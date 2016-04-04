package controllers

import play.api.libs.json.{__, Json, Reads, JsSuccess, JsError}
import play.api.mvc.{Controller, Action}

case class CreateItem(name: String, price: Double)

object CreateItem {
  import play.api.libs.functional.syntax._

  implicit val readsCreateItem: Reads[CreateItem] = //Json.reads[CreateItem]
    // (((__ \ "name").read[String]) and
    //  ((__ \ "price").read[Double])
    // )(CreateItem.apply _)

    // validation
    ((__ \ "name").read(Reads.minLength[String](1)) and
     (__ \ "price").read(Reads.min[Double](0))
    )(CreateItem.apply _)
}

object Items {
  import models.Item

  implicit val writeItem = Json.writes[Item]
}

class Items extends Controller {
  import Items._

  val shop = models.Shop // Refer to your Shop implementation

  // def create = Action(parse.json) {
  //   implicit request =>
  //   request.body.validate[CreateItem] match {
  //     case JsSuccess(createItem, _) =>
  //       shop.create(createItem.name, createItem.price) match {
  //         case Some(item) => Ok(Json.toJson(item))
  //         case None => InternalServerError
  //       }
  //     case JsError(errors) =>
  //       BadRequest
  //   }
  // }

  def create = Action(parse.json[CreateItem]) { implicit request =>
    shop.create(request.body.name, request.body.price) match {
      case Some(item) => Ok(Json.toJson(item))
      case None => InternalServerError
    }
  }

  def list(page: Int) = Action {
    Ok(
      Json.toJson(shop.list)
    )
  }

  def details(id: Long) = Action {
    shop.get(id) match {
      case Some(item) => Ok(Json.toJson(item))
      case None => NotFound
    }
  }

  def update(id: Long) = Action(parse.json[CreateItem]) { implicit request =>
    val item = request.body
    shop.update(id, item.name, item.price) match {
      case Some(item) => Ok(Json.toJson(item))
      case None => InternalServerError
    }
  }

  def delete(id: Long) = Action {
    if (shop.delete(id))
      Ok("ok")
    else
      NotFound
  }
}
