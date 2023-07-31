trait Monad[F[_]] {
  def pure[A](a: A): F[A]
  def map[A, B](fa: F[A])(f: A => B): F[B]
  def flatMap[A, B](fa: F[A])(f: A => F[B]): F[B]
}

case class FutOpt[A](value: Future[Option[A]])

implicit val futOptMonad: Monad[FutOpt] = new Monad[FutOpt] {
  def pure[A](a: A): FutOpt[A] = FutOpt(a.pure[Option].pure[Future])

  def map[A, B](fa: FutOpt[A])(f: A => B): FutOpt[B] =
    FutOpt(fa.value.map(optA: Option[A] => optA.map(f)))

  def flatMap[A, B](fa: FutOpt[A])(f: A => FutOpt[B]): FutOpt[B] =
    FutOpt(fa.value.flatMap {
      case Some(a) => f(a).value
      case None => (None: Option[B]).pure[Future]
    })
}

val f: FutOpt[String] =
  for {
    gab <- FutOpt(getUser("Gabriele"))
    address <- FutOpt(getAddress(gab))
  } yield address.city

val city: Future[Option[String]] = f.value

def getUsers(query: String): List[Option[User]]

case class ListOpt[A](value: List[Option[A]])

implicit val listOptMonad: Monad[ListOpt] = new Monad[ListOpt] {
  def pure[A](a: A): ListOpt[A] = ListOpt(a.pure[Option].pure[List])
  def map[A, B](fa: ListOpt[A])(f: A => B): ListOpt[B] =
    ListOpt(fa.value.map(optA => optA.map(f)))
  def flatMap[A, B](fa: ListOpt[A])(f: A => ListOpt[B]): ListOpt[B] =
    ListOpt(fa.value.flatMap(opt => opt match {
      case Some(a) => f(a).value
      case None => (None: Option[B]).pure[List]
    }))
}

case class WhateverOpt[A, W[_]](value: W[Option[A]])
case class OptionT[F[_], A](value: F[Option[A]])

val f: OptionT[Future, String] =
  for {
    gab <- OptionT(getUser("Gabriele"))
    address <- OptionT(getAddress(gab))
  } yield address.city

val city: Futrue[Option[String]] = f.value

def getUser(id: String): Future[Option[User]]

def getAge(user: User): Future[Int]

def getNickname(user: User): Option[String]

// fail
val lameNickName: Future[Option[String]] =
  for {
    user <- OptionT(getUser("123"))
    age <- OptionT(getAge(user))
    name <- OptionT(getNickname(user))
  } yield s"$name$age"

val lameNickName: OptionT[Future, String] =
  for {
    user <- OptionT(getUser("123"))
    age <- OptionT.liftF(getAge(user))
    name <- OptionT.fromOption(getNickname(user))
  } yield s"$name$age"

case class MyError(msg: String)

def updateUser(u: User): Future[Either[MyError, User]] =
  checkUserExists("foo").flatMap { maybeUser =>
    maybeUser match {
      case Some(user) => checkCanBeUpdated(user).flatMap { canBeUpdated =>
        if(canBeUpdated) {
          updateUserOnDb(user).map(Right(_))
        } else {
          Future.successful(Left(MyError("user cannot be updated")))
        }
      }
      case None => Future.successful(Left(MyError("user does not exists")))
    }
  }

type ResultT[F[_], A] = EigherT[F, MyError, A]
type FutureResult[A] = Result[Future, A]

object FutureResult {
  def apply[A](a: A): FutureResult[A] = apply(Future.successful(a))

  def apply[A](fa: Future[A]): FutureResult[A] = EitherT.liftT(fa)

  def apply[A](e: Either[MyError, A]): FutureResult[A] =
    EitherT.fromEither(e)
}

def checkUserExists(id: String): FutureResult[User] = FutureResult {
  if(id == "123")
    User("123").asRight
  else
    MyError("sorry, no user").asLeft
}

def checkCanBeUpdated(u: User): FutureResult[Boolean] =

def updateUserOnDb(u: User): FutureResult[User] =

def updateUser(user: User): FutureResult[User] =
  for {
    user <- checkUserExists(user.id)
    _ <- checkUserCanBeUpdated(user)
    updatedUser <- updateUser(user)
  }
