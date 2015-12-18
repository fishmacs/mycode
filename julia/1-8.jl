digitsToNum(digits) =
  reduce((num, d) -> num * 10 + d, digits)

check() =
  for digits in permutations([1:8])
    if digitsToNum(digits[1:3]) * digits[4] == digitsToNum(digits[5:end])
      println(digits)
    end
  end

check1() =
  for item in combinations([1:10], 5)
    for arr in permutations(item)
      if digitsToNum(arr) * 4 == digitsToNum(reverse(arr))
        println(arr)
      end
    end
  end
