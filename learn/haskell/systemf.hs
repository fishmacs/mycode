{-# LANGUAGE RankNTypes #-}
{-# LANGUAGE ImpredicativeTypes #-}

type ShowBox = forall b. (forall a. Show a => a -> b) -> b

mkShowBox :: Show a => a -> ShowBox
mkShowBox x = \k -> k x

runShowBox :: forall b. (forall a. Show a => a -> b) -> ShowBox -> b
runShowBox k box = box k

example = [mkShowBox 5, mkShowBox "foo"]

result = map (runShowBox show) example
