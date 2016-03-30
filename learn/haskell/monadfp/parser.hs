data Term = Con Int | Div Term Term

eval :: Term -> M Int
eval (Con a) = return a
eval (Div t u) = do
  x <- eval t
  y <- eval u
  if y == 0 then raise "divide by zero"
  else return x `div` y

answer = (Div (Div (Con 1972) (Con 2)) (Con 23))
error = (Div (Con 1) (Con 0))
        
data M a = Raise Exception | Return a
type Exception = String

return :: a -> M a
return a = Return a

(>>=) :: M a -> (a -> M b) -> M b
m >>= k = case m of
  Raise e -> m
  Return a -> k a

raise :: Exception -> M a
raise e = Raise e
  
type M a = State -> (a, State)
type State = Int

return a = \x -> (a, x)

m >>= k = \x ->
  let (a, y) = m x in
  let (b, z) = k a y in
  (b, z)

tick :: M ()
tick = \x -> ((), x + 1)

eval (Div t u) = do
  tick
  x <- eval t
  y <- eval u
  return x `div` y


type M a = (Output, a)
type Output = String

return a = ("", a)

m >>= k =
  let (x, a) = m in
  let (y, b) = k a in
  (x ++ y, b)

out :: Output -> M ()
out x = (x, ())       

line :: Term -> Int -> Output
line t a = "eval(" ++ showterm t ++ ") <= " ++ showint a ++ "\n"

eval (Con a) = do
  out (line (Con a) a)
  return a
  
eval (Div t u) = do
  x <- eval t
  y <- eval u
  out (line (Div t u) (x `div` y))
  return x `div` y


map :: (a -> b) -> (M a -> M b)
map f m = m >>= \a -> return $ f a       

join :: M (M a) -> M a
join z = z >>= \m -> m

--以下7条是用map/return/join定义的monad laws，如果按照第8条定义>>=，
--则常规的3条Monad laws（return/bind）和map/return/join的定义是等价的
map id = id
map (f . g) = map f . map g
map f . return = return . f
map f . join = join . map $ map f

join . return = id
join . map return = id
join . map join = join . join

m >>= k = join $ map k m
