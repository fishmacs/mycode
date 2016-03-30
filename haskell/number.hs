take 100 [x | n <- [0..], x <- [n*90+9], mod x 8 == 1, mod x 7 == 5, mod x 6 == 3]
  
fib n = fibs !! n
  where fibs = 0 : 1 : zipWith (+) fibs (drop 1 fibs)
