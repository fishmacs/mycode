ave :: Fractional a => [a] -> a
ave [] = 0
ave (x:xs) = (x + ave xs * n) / (n + 1)
  where n = fromInteger $ toInteger $ length xs


palinList :: [a] -> [a]
palinList [] = []
palinList (x:xs) = x:palindrome ++ [x]
  where palindrome = palinList xs


isPalindrome :: Eq a => [a] -> Bool
isPalindrome [] = True
isPalindrome [x] = False
isPalindrome (x:xs) = x == last xs && (isPalindrome $ init xs)


insert :: [a] -> [[a]] -> [[a]]

insert xs [] = [xs]
insert xs (l:ls) =
  if length xs <= length l then
     xs : l : ls
  else
    l: insert xs ls


sortLen :: [[a]] -> [[a]]

sortLen [] = []
sortLen [l] = [l]
sortLen (l:ls) =
  if length l <= length (head ys) then
    l : ys
  else
    head ys : insert l (tail ys)
  where ys = sortLen ls


intersperse :: a -> [[a]] -> [a] 
               
intersperse s [] = []
intersperse s [xs] = xs
intersperse s (x:xs) = x ++ [s] ++ intersperse s xs
