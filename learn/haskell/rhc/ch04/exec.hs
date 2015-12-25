safeHead [] = Nothing
safeHead (x:xs) = Just x

safeTail [] = Nothing
safeTail (x:xs) = Just xs

safeLast [] = Nothing
safeLast list = Just $ last list

safeInit [] = Nothing
safeInit list = Just $ init list

splitWith :: (a -> Bool) -> [a] -> [[a]]
splitWith pred cs =
  let (pre, suf) = break pred cs
  in pre : case suf of
  [] -> []
  _ -> splitWith pred (tail suf)
  
