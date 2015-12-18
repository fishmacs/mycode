lastButOne :: [a] -> [a]

lastButOne [] = error "empty list"
lastButOne [x] = []
lastButOne (x:xs) = x : lastButOne xs
                 
