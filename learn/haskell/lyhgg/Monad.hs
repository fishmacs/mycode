class Monad m where
  return :: a -> m a
  (>>=) :: m a -> (a -> m b) -> m b

  (>>) :: m a -> m b -> m b
  x >> y = x >>= \_ -> y

  fail :: String -> m a
  fail msg = error msg

instance Monad Maybe where
  return = Just
  Nothing >>= f = Nothing
  Just x >>= f = f x
  fail _ = Nothing

type Birds = Int
type Pole = (Birds, Birds)

landLeft :: Birds -> Pole -> Pole
landLeft n (left, right) = (left + n, right)

landRight :: Birds -> Pole -> Pole
landRight n (left, right) = (left, right + n)

x -: f = f x

landLeft :: Birds -> Pole -> Maybe Pole
landLeft n (left, right)
  | abs (left + n - right) < 4 = Just (left + n, right)
  | otherwise = Nothing
                               
landRight :: Birds -> Pole -> Maybe Pole
landRight n (left, right)
  | abs (left - right - n) < 4 = Just (left, right + n)
  | otherwise = Nothing


foo :: Maybe String
foo = Just 3 >>= (\x ->
      Just "!" >>= (\y ->
      Just (show x ++ y)))

foo = do
  x <- Just 3
  y <- Just "!"
  Just (show x ++ y)
  
routine :: Maybe Pole
routine = do           
  start <- return (0, 0)
  first <- landLeft 2 start
  Nothing
  second <- landRight 2 first
  landLeft 1 second

instance Monad [] where
  return x = [x]
  xs >>= f = concat $ map f xs
  fail _ = []
  
[1,2] >>= \n -> ['a', 'b'] >>= \ch -> return (n,ch)

do
  n <- [1,2]
  ch <= ['a', 'b']
  return (n, ch)

[(n, ch) | n <- [1,2], ch <- ['a', 'b']]


class Monad m => MonadPlus m where
  mzero :: m a
  mplus :: m a -> m a -> m a

instance MonadPlus [] where
  mzero = []
  mplus = (++)
  
instance MonadPlus Maybe where
  mzero = Nothing
  Nothing `mplus` m = m
  m `mplus` Nothing = m
  Just a `mplus` Just b = Just b 

guard :: (MonadPlus m) => Bool -> m ()
guard True = return ()         
guard False = mzero

[1..50] >>= (\x -> guard ('7' `elem` show x) >> return x)

sevenOnly = do
  x <- [1..50]
  guard ('7' `elem` show x)
  return x


(<=<) :: (Monad m) => (b -> m c) -> (a -> m b) -> (a -> m c)
f <=< g = \x -> g x >>= f

-- Monad laws

-- left identity
return x >>= f === f x

f <=< return === f

f.id === f

-- right identity
m >>= return === m  

return <=< f === f

id.f === f
  
  
-- associativity
(m >>= f) >>= g === m >>= (\x -> f x >>= g)

f <=< (g <=< h) === (f <=< g) <=< h

(f.g).h === f.(g.h)

