package models

import scala.collection.concurrent.TrieMap
import java.util.concurrent.atomic.AtomicLong
import javax.inject.Inject

import play.api.db.slick.{DatabaseConfigProvider, HasDatabaseConfigProvider}
import play.api.libs.concurrent.Execution.Implicits.defaultContext
import slick.driver.JdbcProfile

import scala.concurrent.Future
import scala.util.{Failure, Success}

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

class Shop @Inject() (protected val dbConfigProvider: DatabaseConfigProvider) extends HasDatabaseConfigProvider[JdbcProfile] {

  import driver.api._

  private class ShopTable(tag: Tag) extends Table[Item](tag, "shop") {
    def id = column[Long]("id", O.PrimaryKey, O.AutoInc)

    def name = column[String]("name")

    def price = column[Double]("price")

    def * = (id, name, price) <>((Item.apply _).tupled, Item.unapply)
  }

  private val items = TableQuery[ShopTable]

  def list(): Future[Seq[Item]] = db.run(items.result)

  def create(name: String, price: Double): Future[Item] = db.run {
    (items.map(item => (item.name, item.price))
       returning items.map(_.id)
       into ((tuple, id) => Item(id, tuple._1, tuple._2))
    ) += (name, price)
  }

  def get(id: Long): Future[Option[Item]] = db.run {
    items.filter(_.id === id).take(1).result.headOption
  }

  def update(id: Long, name: String, price: Double): Future[Option[Item]] = {
    val f: Future[Int] = db.run {
      items.filter(_.id === id).map(i => (i.name, i.price)).update((name, price))
    }
    f.map(v => if (v > 0) Some(Item(id, name, price)) else None)
  }

  def delete(id: Long): Future[Boolean] = {
    val v = db.run(items.filter(_.id === id).delete)
    v.map(i => i > 0)
  }
}
