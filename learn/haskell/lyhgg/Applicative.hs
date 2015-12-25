class (Functor f) => Applicative f where
  pure :: a -> f a
  (<*>) :: f (a -> b) -> f a -> f b

instance Applicative Maybe where
  pure = Just
  Nothing <*> _ = Nothing
  (Just f) <*> something = fmap f something

(<$>) :: (Functor f) => (a -> b) -> f a -> f b
f <$> x = fmap f x

instance Applicative [] where
  pure x = [x]
  fs <*> xs = [f x | f <- fs, x <- xs]
  
instance Applicative IO where
  pure = return

  a <*> b = do
    f <- a
    x <- b
    return (f x)

myAction :: IO String
myAction = do
  a <- getLine
  b <- getLine
  return $ a ++ b
myAction' = (++) <$> getLine <*> getLine

instance Applicative ((->) r) where
  pure x = \_ -> x
  f <*> g = \x -> f x (g x)


newtype ZipList a = ZipList { getZipList :: [a] }

instance Functor ZipList where
  fmap f (ZipList xs) = ZipList $ map f xs
  
instance Applicative ZipList where
  pure x = ZipList (repeat x)
  ZipList fs <*> ZipList xs = ZipList (zipWith (\f x -> f x) fs xs)

liftA2 :: (Applicative f) => (a -> b -> c) -> f a -> f b -> f c
liftA2 f a b = f <$> a <*> b

sequenceA :: (Applicative f) => [f a] -> f [a]
--sequenceA [] = pure []
--sequenceA (x:xs) = (:) <$> x <*> sequenceA xs
sequenceA = foldr (liftA2 (:)) (pure [])
           
