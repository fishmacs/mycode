{-# LANGUAGE RankNTyes, TypeOperators #-}

import Control.Monad (join)
  
-- | A natural transformations between two 'Functor' instances. Law:
--  
-- > fmap f . eta g == eta g . fmap f
--
-- Neat fact: the type system actually guarantees this law.
--

newtype f :-> g = Natural { eta :: forall x . f x -> g x }

listToMaybe :: [] :-> Maybe
listToMaybe = Natural go
  where go [] = Nothing
        go (x:_) = Just

maybeToList :: Maybe :-> []
maybeToList = Natural go
  where go Nothing = []
        go (Just x) = [x]

reverse' :: [] :-> []
reverse' = Natural reverse

newtype Identity a = Identity { runIdentity :: a }

instance Functor Identity where
  fmap f (Identity a) = Identity (f a)

return' :: Monad t => Identity :-> t
return' = Natural (return . runIdentity)

newtype Compose f g a = Compose { getCompose :: f (g a) }

instance (Functor f, Functor g) => Functor (Compose f g) where
  fmap f (Compose fga) = Compose (fmap (fmap f) fga)

join' :: Monad t => Compose t t :-> t
join' = Natural (join . getCompose)


-- Monoid laws
-- 1. Compose f (Compose g h) === Compose (Compose f g) h
-- 2. Compose f Identity === f
-- 3. Compose Identity g === g

