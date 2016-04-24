package controllers

import javax.inject.Inject

import models.Shop
import play.api.libs.json.{JsError, JsSuccess, Json, Reads, __}
import play.api.mvc.{Action, Controller}
import play.api.libs.concurrent.Execution.Implicits.defaultContext

import scala.util.{Failure, Success}

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

class Items @Inject() (shop: Shop) extends Controller {
  import Items._

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

  def create = Action.async(parse.json[CreateItem]) { implicit request =>
    shop.create(request.body.name, request.body.price).map(item => Ok(Json.toJson(item)))
  }

  def list(page: Int) = Action.async {
    shop.list.map(items => Ok(Json.toJson(items)))
  }

  def details(id: Long) = Action.async {
    shop.get(id).map(_ match {
      case Some(item) => Ok(Json.toJson(item))
      case None => NotFound
    })
  }

  def update(id: Long) = Action.async(parse.json[CreateItem]) { implicit request =>
    val item = request.body
    shop.update(id, item.name, item.price).map(_ match {
      case Some(item) => Ok(Json.toJson(item))
      case None => InternalServerError
    })
  }

  def delete(id: Long) = Action.async {
    shop.delete(id).map(_ match {
      case true => Ok("ok")
      case false => NotFound
    })
  }
}
