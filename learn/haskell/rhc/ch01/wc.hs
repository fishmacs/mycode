import Text.Printf

main :: IO()
main = interact wordCount
  where wordCount input = printf "(%d, %d, %d)\n" lineNum wordNum charNum
          where lineNum = length $ lines input
                wordNum = length $ words input
                charNum = length input
