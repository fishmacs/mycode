type State = Arr
type Ix = Id
type Val = Int

newarray :: Val -> Arr
index :: Ix -> Arr -> Val
update :: Ix -> Val -> Arr -> Arr

index i (newarray v) = v
--index i (update i v x) = v
index i (update j v x) =
  if i <> j then index i x
  else v

data Term = Var Id | Con Int | Add Term Term
data Comm = Asgn Id Term | Seq Comm Comm | If Term Comm Comm
data Prog = Prog Comm Term

eval :: Term -> State -> Int
eval (Var i) x = index i x
eval (con a) x = a
eval (add t u) x = eval t x + eval u x

exec :: Comm -> State -> State
exec (Asgn i t) x = update i (eval t x) x
exec (seq c d) x = exec d (exec c)
exec (If t c d) x =
  if eval t x == 0 then exec c x
  else exec d x

elab :: Prog -> Int
elab (Prog c t) = eval t (exec c (newarray 0))
                  
type M a = State -> (a, State)
type State = Arr

return a = \x -> (a, x)           
m >>= k = \x ->
  let (a, y) = m x in
  let (b, z) = k a y in
  (b, z)

block :: Val -> M a -> a
block v m = let (a, x) = m (newarray v) in a

fetch :: Ix -> M Val
fetch i = \x -> index i x, x

assign :: Ix -> Val -> M()
asign i v = \x -> ((), update i v x)          

eval :: Term -> M Int
eval (Var i) = fetch i
eval (Con a) = return a
eval (Add t u) = do
  x <- eval t
  y <- eval y
  return (x + y)

exec :: Comm -> M ()
exec (Asgn i t) = eval t >>= \a -> assign i a
exec (Seq c d) = do
  exec c
  exec d
  return ()
exec (If t c d)  = do
  a <- eval t
  if a == 0 then exec c else exec d

elab :: Prog -> Int
elab (Prog c t) = block 0 do
  exec c
  a <- eval t
  return a

type M' a = State -> a

return' a = \x -> a

m >>=' k = \x ->
  let a = mx in k a x

fetch' i = \x -> index i x

coerce :: M' a -> M a
coerce m = \x -> let a = m x in (a, x)

eval (Var i) = fetch' i
eval (Con a) = return' a
eval (Add t u) = eval t >>=' \a -> eval u >>=' \b -> return' (a + b)

exec (Assign i t) = coerce (eval t) >>= \a -> assign i a
exec (Seq c d) = exec c >>= \() -> exec d >>= \() -> return ()
exec (If t c d) = coerce (eval) >>= \a -> if a == 0 then exec c else execd

elab (Prog c t) = block 0 (exec c >>= \() -> coerce (eval t) >>= \a -> return a)
