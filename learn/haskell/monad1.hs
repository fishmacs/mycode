{_# OPTIONS_GHC -fglasgow-exts #-}

import Control.Monad
import Test.QuickCheck

class Monoid m where
  one :: () -> m
  mult :: (m, m) -> m

-- monoidial category

lambda :: a -> ((), a)
lambda x = ((), x)

rho :: a -> (a, ())
rho x = (x, ())

alpha :: ((a, b), c) -> (a, (b, c))
alpha ((x, y), z) = (x, (y, z))

(<#>) :: (a -> c) -> (b -> d) -> (a, b) -> (c, d)
(f <#> g) (x, y) = (f x, g y)

law1_left, law1_middle, law1_right :: m -> m

law1_left = mult . (one <#> id) . lambda
law1_middle = id
law1_right = mult . (id <#> one) . rho

law2_left, law2_right :: ((m, m), m) -> m
law2_left = mult . (mult <#> id)
law2_right = mult . (id <#> mult) . alpha


-- endofunctor category

type (f :<*> g) x = f (g x)

(<*>) :: (forall x . a x -> c x) -> (forall x . b x -> d x) -> (forall x . a (b x) -> c (d x))
(<*>) :: (Functor a, Functor b, Functor c, Functor d) => (a (d x) -> c (d y)) -> (b z -> d x) -> a (b z) -> c (d y)
(<*>) :: Functor a => (forall x.a x -> c x) -> (forall x.b x -> d x) -> (forall x.a (b x) -> c (d x))
(<*>) f g = f . fmap g

newtype Id x = Id x deriving Show

instance Functor Id where
  fmap f (Id x) = Id (f x)

lambda' :: Functor F => f a -> Id (f a)
lambda' x = Id x

rho' :: Functor f => f a -> f (Id a)
rho' x = fmap Id x

alpha' :: f (g (h a)) -> f (g (h a))
alpha' = id

class Functor m => Monoid' m where
  one' :: Id a -> m a
  mult' :: m (m a) -> m a

  law1_left', law1_middle', law1_right' :: m a -> m a
  law1_left' = mult' . (one' <*> id). lambda'

  law1_middle' = id

  law1_right' = mult' . (id <*> one') . rho'

  law2_left', law2_right' :: ((m :<*> m) :<*> m) a -> m a
  law2_left' = mult' . (mult' <*> id)
  law2_right' = mult' . (id <*> mult') . alpha'

newtype  Monad m => TranslateMonad m a = TM {unTM :: m a} deriving (Eq, Show)

translate :: Monad m => m a -> TranslateMonad m a
translate x = TM x

instance (Monad m, Functor m) => Functor (TranslateMonad m) where
  fmap f (TM x) = TM (fmap f x)

instance (Functor m, Monad m) => Monoid' (TranslateMonad m) where
  one' (Id x) = TM $ return x
  mult' (TM x) = TM $ fmap unTM x >>= id

instance Arbitrary a => Arbitrary (Id a) where
  arbitrary = liftM Id arbitrary

instance (Monad m, Eq (m a), Arbitrary (m a)) => Arbitrary (TranslateMonad m a) where
  arbitrary = liftM TM arbitrary

check4 = quickCheck $ \n -> law1_left' n == law1_middle' (n :: TranslateMonad [] Int)
check5 = quickCheck $ \n -> law1_left' n == law1_right' (n :: TranslateMonad [] Int)
check6 = quickCheck $ \n -> law2_left' n == law2_right' (n :: TranslateMonad [] Int)

