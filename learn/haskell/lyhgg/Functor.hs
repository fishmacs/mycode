class Functor f where
  fmap :: (a -> b) -> f a -> f b

instance Functor [] where
  fmap = map

instance Functor IO where
  fmap f action = do
    result <- action
    return (f result)

instance Functor ((->)r) where
  fmap = (.)

instance Functor Maybe where 
  fmap f (Just x) = Just (f x)
  fmap f Nothing = Nothing

instance Functor (Either a) where
  fmap f (Right x) = Right (f x)
  fmap f (Left x) = Left x

class Tofu t where
  tofu :: j a -> t a j

data Frank a b = Frank { frankField :: b a } deriving (Show)

instance Tofu Frank where
  tofu x = Frank x
  
data Barry t k p = Barry { yabba :: p, dabba :: t k }

instance Functor (Barry a b) where
  fmap f (Barry {yabba = x, dabba = y}) = Barry {yabba = f x, dabba = y}
  
