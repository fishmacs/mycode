package models

import scala.collection.concurrent.TrieMap
import java.util.concurrent.atomic.AtomicLong

case class Item(id: Long, name: String, price: Double)

// class Shop(schema: Schema) {
//   import schema.{db. items}
//   import schema.queryLanguage._

//   def list(): Iterable[Item] = db withSession {
//     implicit session => items.list()
//   }

//   def create(name: String, price: Double): Option[Item] =
//     db withSession {
//       implicit session =>
//       val id = items.returning(items.map(_.id)) += Item(0, name, price)
//       items.byId(id).firstOption()
//     }

//   def get(id: Long): Option[Item] =
//     db withSession {
//       implicit session => items.byId(id).firstOption()
//     }

//   def update(id: Long, name: String, price: Double): Option[Item] =
//     db.withSession {
//       implicit session =>
//       items.byId(id).update(Item(id, name, price))
//       items.byId(id).firstOption()
//     }

//   def delete(id: Long): Boolean =
//     db withSession {
//       implicit session => items.byId(id).delete != 0
//     }
// }

trait Shop {
  def list(): Seq[Item]
  def create(name: String, price: Double): Option[Item]
  def get(id: Long): Option[Item]
  def update(id: Long, name: String, price: Double): Option[Item]
  def delete(id: Long): Boolean
}

object Shop extends Shop {
  private val items = TrieMap.empty[Long, Item]
  private val seq = new AtomicLong

  def list(): Seq[Item] = items.values.to[Seq]

  def create(name: String, price: Double): Option[Item] = {
    val id = seq.incrementAndGet()
    val item = Item(id, name, price)
    items.put(id, item)
    Some(item)
  }

  def get(id: Long): Option[Item] = items.get(id)

  def update(id: Long, name: String, price: Double): Option[Item] = {
    val item = Item(id, name, price)
    items.replace(id, item)
    Some(item)
  }

  def delete(id: Long): Boolean = items.remove(id).isDefined
}
