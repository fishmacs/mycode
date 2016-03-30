:m Data.List

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

type KnightPos = (Int, Int)

-- moveKnight (c, r) = do
--   (c', r') <- [(c+2, r-1), (c+2, r+1), (c-2, r-1), (c-2, r+1)
--               ,(c+1, r-2), (c+1, r+2), (c-1, r-2), (c-1, r+2)]
--   guard (c' `elem` [1..8] && r' `elem` [1..8])
--   return (c', r')

moveKnight (c, r) = filter onBoard
  [(c+2, r-1), (c+2, r+1), (c-2, r-1), (c-2, r+1)
  ,(c+1, r-2), (c+1, r+2), (c-1, r-2), (c-1, r+2)]
  where onBoard (c, r) = c `elem` [1..8] && r `elem` [1..8]

moveKnightPath path@((x, y): pts) = [next: path | next <- moveKnight (x, y)]

in3 start = [[start]] >>= moveKnightPath >>= moveKnightPath >>= moveKnightPath

check p1 p2 = filter (\(p:ps) -> p == p2) (in3 p1)
