type M a = State -> [(a, State)]
type State = String

data Term = Con Int | Div Term Term

term :: M Term

item :: M Char
item [] = []
item (a:x) = [(a, x)]

return :: a -> M a
return a x = [(a, x)]

(>>=) :: M a -> (a -> M b) -> M b
m >>= k = \x -> [(b, z) | (a, y) <- m x, (b, z) <- k a y]

twoItems :: M (Char, Char)
twoItems = item >>= \a -> item >>= \b -> return (a, b)

zero :: M a
zero x = []

(@) :: M a -> M a -> M a
m @ n = \x -> m x ++ n x

oneOrTwoItems :: M String
oneOrTwoItems = (item >>= \a -> return [a]) @
                (item >>= \a -> item >>= \b -> return [a, b])

-- filter
(>>) :: M a -> (a -> Bool) -> M a
m >> p = m >>= \a -> if p a then return a else zero

letter :: M Char
letter = item >> isLetter

digit :: M Int
digit = (item >> isDigit) >>= \a -> return (ord a - ord '0')

lit :: Char -> M Char
lit c = item >> (==c)

iterate :: M a -> M [a]
iterate m = (m >>= \a -> iterate m >>= \x -> return (a:x)) @ return []

number :: M Int
number = digit >>= \a -> iterate digit >>= \x -> return $ asNumber (a:x)

(#) :: M a -> M a -> M a
m # n = \x -> if m x != [] then m x else n x

reiterate :: M a -> M [a]
reiterate m = (m >>= \a -> reiterate m >>= \x -> return (a:x) # return [])

number':: M Int
number' = digit >>= \a -> reiterate digit >>= \x -> return $ asNumber (a:x)

(m @ n) >>= k = (m >>= k) @ (n >>= k)
m >>= \a -> k a @ h a = (m >>= k) @ (m >>= h)

m >>= \a -> k a # h a = (m >>= k) # (m >>= h)

term ::= number | '(' term / term ')'
term :: M Term
term = (number >>= \a -> return (Con a)) @
       (lit '(' >>= \_ -> term >>= \t -> lit '/' >>= \_ -> term >>= \u -> lit ')' >>= \_ -> return (Div t u))

term ::= term '/' factor | factor
factor ::= number | '(' term ')'

term :: M Term
term = (term >>= \t -> lit '/' >>= \_ -> factor >>= \u -> return (Div t u)) @ factor

factor :: M Term
factor = (number >>= \a -> return (Con a)) @
         (lit '(' >>= \_ -> term >>= \t -> lit ')' >>= \_ -> return t)

term ::= factor term'
term' ::= '/' factor term' | return

term :: M Term
term = factor >>= \t -> term' t

term' :: Term -> M Term
term' t = (lit '/' >>= \_ -> factor >>= \u -> term' (Div t u)) @ return t

-- left-recursive
m = (m >>= k) @ n
-- ---------->
m = n >>= (closure k)

closure :: (a -> M a) -> (a -> M a)
closure k a = (k a >>= closure k) @ return a

guarantee :: M a -> M a
guarantee m x = let u = mx in (fst $ head u, snd $ head u): tail u

reiterate :: M a -> M [a]
reiterate m = guarantee ((m >>= \a -> reiterate m >>= \x -> return (a:x)) # return [])
